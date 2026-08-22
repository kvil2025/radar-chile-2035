import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.models import Indicator, Observation, Score
from packages.common.database import SessionLocal
from packages.scoring.normalizers import normalize_min_max

logger = logging.getLogger(__name__)

class ScoringEngine:
    """
    Quantitative Scoring Engine (Methodology v0.1).
    Computes the 5 canonical indices with complete mathematical explainability.
    """

    METHODOLOGY_VERSION = "v0.1"

    CONFIGS = {
        "DOLLAR_STRESS": {
            "name": "Dollar Stress Index",
            "description": "Nivel de escasez, costo y tensión de liquidez en dólares a escala global.",
            "components": [
                {"code": "DXY", "weight": 0.30, "min": 90.0, "max": 115.0, "direction": 1},
                {"code": "US10Y", "weight": 0.25, "min": 2.0, "max": 6.0, "direction": 1},
                {"code": "US30Y", "weight": 0.15, "min": 2.5, "max": 6.5, "direction": 1},
                {"code": "US_CPI", "weight": 0.15, "min": 1.5, "max": 7.0, "direction": 1},
                {"code": "FOREIGN_TREASURY_HOLDINGS", "weight": 0.15, "min": 7.0, "max": 9.5, "direction": -1},
            ]
        },
        "MONETARY_STRESS": {
            "name": "Monetary Stress Index",
            "description": "Fragilidad estructural del sistema monetario y dominancia fiscal.",
            "components": [
                {"code": "US_FISCAL_DEFICIT", "weight": 0.20, "min": -10.0, "max": -2.0, "direction": -1},
                {"code": "US_DEBT", "weight": 0.15, "min": 90.0, "max": 140.0, "direction": 1},
                {"code": "GOLD", "weight": 0.25, "min": 1800.0, "max": 3000.0, "direction": 1},
                {"code": "US_FED_RATE", "weight": 0.20, "min": 1.0, "max": 6.5, "direction": 1},
                {"code": "USD_RESERVES_SHARE", "weight": 0.20, "min": 50.0, "max": 65.0, "direction": -1},
            ]
        },
        "COMMODITY_CYCLE": {
            "name": "Commodity Cycle Index",
            "description": "Fuerza y tracción del ciclo global de materias primas e insumos industriales.",
            "components": [
                {"code": "COPPER", "weight": 0.35, "min": 3.0, "max": 5.50, "direction": 1},
                {"code": "GOLD", "weight": 0.15, "min": 1800.0, "max": 3000.0, "direction": 1},
                {"code": "OIL", "weight": 0.20, "min": 50.0, "max": 110.0, "direction": 1},
                {"code": "IRON_ORE", "weight": 0.15, "min": 75.0, "max": 145.0, "direction": 1},
                {"code": "CHINA_PMI", "weight": 0.15, "min": 45.0, "max": 55.0, "direction": 1},
            ]
        },
        "MINING_CYCLE": {
            "name": "Mining Cycle Index",
            "description": "Salud productiva, inversión y tracción de exportaciones del sector minero.",
            "components": [
                {"code": "COPPER", "weight": 0.30, "min": 3.0, "max": 5.50, "direction": 1},
                {"code": "CHILE_COPPER_PRODUCTION", "weight": 0.25, "min": 380.0, "max": 520.0, "direction": 1},
                {"code": "CHILE_MINING_CAPEX", "weight": 0.25, "min": 45.0, "max": 80.0, "direction": 1},
                {"code": "CHINA_COPPER_IMPORTS", "weight": 0.20, "min": -15.0, "max": 25.0, "direction": 1},
            ]
        },
        "CHILE_OPPORTUNITY": {
            "name": "Chile Opportunity Index",
            "description": "Índice sintético de oportunidad económica, inversión y dinamismo para Chile.",
            "components": [
                {"code": "COPPER", "weight": 0.30, "min": 3.0, "max": 5.50, "direction": 1},
                {"code": "CHILE_MINING_CAPEX", "weight": 0.20, "min": 45.0, "max": 80.0, "direction": 1},
                {"code": "CLP_USD", "weight": 0.15, "min": 780.0, "max": 1050.0, "direction": -1},
                {"code": "CHILE_ELECTRICITY_DEMAND", "weight": 0.15, "min": 6200.0, "max": 7500.0, "direction": 1},
                {"code": "CHILE_IMACEC", "weight": 0.10, "min": -2.0, "max": 6.0, "direction": 1},
                {"code": "US10Y", "weight": 0.10, "min": 2.5, "max": 5.5, "direction": -1},
            ]
        }
    }

    def __init__(self, db: Optional[Session] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()

    def run_all(self) -> dict[str, float]:
        """Compute all 5 scores, save to database, and return summary dict."""
        logger.info("🎯 Running Quantitative Scoring Engine...")
        results = {}
        latest_obs = self._get_latest_observations()

        for score_type, config in self.CONFIGS.items():
            score_data = self._calculate_single_score(score_type, config, latest_obs)
            results[score_type] = score_data["value"]

            # Persist to database
            score_record = Score(
                score_type=score_type,
                timestamp=datetime.datetime.utcnow(),
                value=score_data["value"],
                confidence=score_data["confidence"],
                methodology_version=self.METHODOLOGY_VERSION,
                metadata_json=score_data
            )
            self.db.add(score_record)

        self.db.commit()
        logger.info(f"✅ Quantitative Scores updated: {results}")
        return results

    def _calculate_single_score(self, score_type: str, config: dict, latest_obs: dict) -> dict:
        contributors = []
        total_weighted_points = 0.0
        total_weight = 0.0
        valid_count = 0

        for comp in config["components"]:
            code = comp["code"]
            weight = comp["weight"]
            min_val = comp["min"]
            max_val = comp["max"]
            direction = comp["direction"]

            obs = latest_obs.get(code)
            if obs:
                raw_val = obs.value
                norm_val = normalize_min_max(raw_val, min_val, max_val, direction=direction)
                contribution_pts = round(norm_val * weight, 2)
                
                total_weighted_points += contribution_pts
                total_weight += weight
                if obs.quality_status == "VALID":
                    valid_count += 1

                contributors.append({
                    "indicator_code": code,
                    "indicator_name": obs.indicator.name if obs.indicator else code,
                    "weight": weight,
                    "raw_value": round(raw_val, 4),
                    "normalized_value": norm_val,
                    "contribution_points": contribution_pts,
                    "direction": direction,
                    "unit": obs.indicator.unit if obs.indicator else "",
                    "quality_status": obs.quality_status
                })
            else:
                # Fallback to neutral 50
                norm_val = 50.0
                contribution_pts = round(norm_val * weight, 2)
                total_weighted_points += contribution_pts
                total_weight += weight

                contributors.append({
                    "indicator_code": code,
                    "indicator_name": code,
                    "weight": weight,
                    "raw_value": 0.0,
                    "normalized_value": norm_val,
                    "contribution_points": contribution_pts,
                    "direction": direction,
                    "unit": "",
                    "quality_status": "MISSING"
                })

        final_score = round(total_weighted_points / total_weight if total_weight > 0 else 50.0, 1)
        confidence = round(valid_count / len(config["components"]), 2) if config["components"] else 1.0

        # Calculate 30-day delta if past scores exist
        past_score = self.db.query(Score).filter(
            Score.score_type == score_type,
            Score.timestamp <= datetime.datetime.utcnow() - datetime.timedelta(days=20)
        ).order_by(Score.timestamp.desc()).first()

        delta_30d = round(final_score - past_score.value, 1) if past_score else 0.0
        trend = "UP" if delta_30d > 1.5 else ("DOWN" if delta_30d < -1.5 else "STABLE")

        return {
            "score_type": score_type,
            "name": config["name"],
            "description": config["description"],
            "value": final_score,
            "confidence": confidence,
            "methodology_version": self.METHODOLOGY_VERSION,
            "contributors": contributors,
            "trend": trend,
            "delta_30d": delta_30d,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    def _get_latest_observations(self) -> dict[str, Observation]:
        indicators = self.db.query(Indicator).all()
        latest_map = {}
        for ind in indicators:
            latest = self.db.query(Observation).filter(
                Observation.indicator_id == ind.id
            ).order_by(Observation.timestamp.desc()).first()
            if latest:
                latest_map[ind.code] = latest
        return latest_map

    def close(self):
        if not self.db_provided:
            self.db.close()
