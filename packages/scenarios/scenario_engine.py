import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.models import Scenario, Indicator, Observation
from packages.common.database import SessionLocal

logger = logging.getLogger(__name__)

class ScenarioEngine:
    """
    Evaluates empirical evidence across the 4 canonical macro scenarios (S1-S4).
    Calculates dynamic probabilities explicitly tagged as MODEL_ESTIMATE.
    """

    METHODOLOGY_VERSION = "v0.1"

    def __init__(self, db: Optional[Session] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()

    def evaluate_scenarios(self) -> list[dict]:
        """Evaluate each scenario based on current indicators and persist updated probabilities."""
        logger.info("🔮 Evaluating Macro Scenarios S1-S4...")
        latest_obs = self._get_latest_observations()

        copper = latest_obs.get("COPPER", 4.35)
        gold = latest_obs.get("GOLD", 2450.0)
        us10y = latest_obs.get("US10Y", 4.25)
        us30y = latest_obs.get("US30Y", 4.50)
        us_cpi = latest_obs.get("US_CPI", 2.9)
        dxy = latest_obs.get("DXY", 104.2)
        china_pmi = latest_obs.get("CHINA_PMI", 50.8)
        ai_capex = latest_obs.get("AI_DATA_CENTER_CAPEX_PROXY", 34.0)

        # 1. Raw evidence points for each scenario
        raw_weights = {
            "S1_SOFT_LANDING": 25.0,
            "S2_FISCAL_DOMINANCE": 20.0,
            "S3_GLOBAL_RECESSION": 10.0,
            "S4_COMMODITY_SUPERCYCLE": 20.0
        }

        # S1 Soft Landing adjustments
        if 2.0 <= us_cpi <= 3.2:
            raw_weights["S1_SOFT_LANDING"] += 15.0
        if 3.8 <= us10y <= 4.4:
            raw_weights["S1_SOFT_LANDING"] += 10.0

        # S2 Fiscal Dominance adjustments
        if us30y > 4.45:
            raw_weights["S2_FISCAL_DOMINANCE"] += 15.0
        if gold > 2400.0:
            raw_weights["S2_FISCAL_DOMINANCE"] += 15.0

        # S3 Global Recession adjustments
        if china_pmi < 49.0:
            raw_weights["S3_GLOBAL_RECESSION"] += 25.0
        if copper < 3.80:
            raw_weights["S3_GLOBAL_RECESSION"] += 20.0

        # S4 Commodity Supercycle adjustments
        if copper > 4.25:
            raw_weights["S4_COMMODITY_SUPERCYCLE"] += 20.0
        if ai_capex > 25.0:
            raw_weights["S4_COMMODITY_SUPERCYCLE"] += 15.0
        if china_pmi >= 50.5:
            raw_weights["S4_COMMODITY_SUPERCYCLE"] += 10.0

        # Normalize probabilities so sum = 1.0
        total_raw = sum(raw_weights.values())
        probabilities = {k: round(v / total_raw, 3) for k, v in raw_weights.items()}

        results = []
        scenarios = self.db.query(Scenario).all()

        for sc in scenarios:
            if sc.scenario_code in probabilities:
                sc.probability = probabilities[sc.scenario_code]
                sc.probability_type = "MODEL_ESTIMATE"
                sc.updated_at = datetime.datetime.utcnow()
                self.db.add(sc)

                results.append({
                    "scenario_code": sc.scenario_code,
                    "name": sc.name,
                    "description": sc.description,
                    "probability": sc.probability,
                    "probability_type": "MODEL_ESTIMATE",
                    "expected_chile_effect": sc.expected_chile_effect,
                    "risk_level": sc.risk_level,
                    "opportunity_level": sc.opportunity_level,
                    "drivers": sc.drivers,
                    "supporting_indicators": sc.supporting_indicators,
                    "contradicting_indicators": sc.contradicting_indicators,
                })

        self.db.commit()
        logger.info(f"✅ Scenarios updated: {probabilities}")
        return results

    def _get_latest_observations(self) -> dict[str, float]:
        indicators = self.db.query(Indicator).all()
        obs_map = {}
        for ind in indicators:
            latest = self.db.query(Observation).filter(
                Observation.indicator_id == ind.id
            ).order_by(Observation.timestamp.desc()).first()
            if latest:
                obs_map[ind.code] = latest.value
        return obs_map

    def close(self):
        if not self.db_provided:
            self.db.close()
