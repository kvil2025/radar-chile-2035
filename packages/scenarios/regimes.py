import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.models import Indicator, Observation, Regime, Score
from packages.common.database import SessionLocal

logger = logging.getLogger(__name__)

class EconomicRegimeClassifier:
    """
    Classifies global economic conditions into one of 8 canonical regimes based on empirical evidence.
    Ensures non-dogmatic, probabilistic phrasing ('Las condiciones son consistentes con...').
    """

    REGIMES = [
        "NORMAL",
        "EXPANSION",
        "TRANSITION",
        "FISCAL_STRESS",
        "INFLATIONARY",
        "RECESSION",
        "COMMODITY_SUPERCYCLE",
        "MONETARY_STRESS"
    ]

    def __init__(self, db: Optional[Session] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()

    def classify(self) -> dict:
        """Run rule-based probabilistic classification across empirical observations and scores."""
        logger.info("🧭 Running Economic Regime Classifier...")
        latest_obs = self._get_latest_observations()

        # Extract key variables with safe fallbacks
        copper = latest_obs.get("COPPER", 4.35)
        gold = latest_obs.get("GOLD", 2450.0)
        us10y = latest_obs.get("US10Y", 4.25)
        us30y = latest_obs.get("US30Y", 4.50)
        us_cpi = latest_obs.get("US_CPI", 2.9)
        dxy = latest_obs.get("DXY", 104.2)
        china_pmi = latest_obs.get("CHINA_PMI", 50.8)
        ai_capex = latest_obs.get("AI_DATA_CENTER_CAPEX_PROXY", 34.0)
        deficit = latest_obs.get("US_FISCAL_DEFICIT", -6.2)
        imacec = latest_obs.get("CHILE_IMACEC", 2.4)

        # Evaluate regime probabilities
        regime_scores: dict[str, float] = {r: 10.0 for r in self.REGIMES}

        # 1. COMMODITY SUPERCYCLE EVIDENCE
        if copper > 4.20 and ai_capex > 25.0 and china_pmi >= 50.0:
            regime_scores["COMMODITY_SUPERCYCLE"] += 45.0
            if copper > 4.50:
                regime_scores["COMMODITY_SUPERCYCLE"] += 20.0

        # 2. MONETARY STRESS EVIDENCE
        if gold > 2400.0 and dxy > 103.5 and us10y > 4.20:
            regime_scores["MONETARY_STRESS"] += 40.0
            if gold > 2500.0:
                regime_scores["MONETARY_STRESS"] += 15.0

        # 3. FISCAL STRESS EVIDENCE
        if deficit < -5.5 and us30y > 4.40:
            regime_scores["FISCAL_STRESS"] += 35.0

        # 4. INFLATIONARY EVIDENCE
        if us_cpi > 3.5:
            regime_scores["INFLATIONARY"] += 40.0

        # 5. RECESSION EVIDENCE
        if china_pmi < 49.0 and copper < 3.80:
            regime_scores["RECESSION"] += 50.0

        # 6. EXPANSION EVIDENCE
        if china_pmi > 51.5 and imacec > 3.0 and us_cpi < 3.0:
            regime_scores["EXPANSION"] += 35.0

        # Find winning regime
        sorted_regimes = sorted(regime_scores.items(), key=lambda x: x[1], reverse=True)
        top_regime, top_score = sorted_regimes[0]
        second_regime, second_score = sorted_regimes[1]

        # Calculate normalized confidence
        total_score = sum(regime_scores.values())
        confidence = round(min(0.95, max(0.60, top_score / total_score * 2.5)), 2)

        # Primary driver determination
        if top_regime == "COMMODITY_SUPERCYCLE":
            primary_driver = "Tracción estructural en demanda de cobre por electrificación y centros de datos de IA"
            rationale = (
                f"Las condiciones macroeconómicas observadas son consistentes con un régimen de COMMODITY_SUPERCYCLE "
                f"(Nivel de confianza: {int(confidence*100)}%), impulsado principalmente por la cotización del cobre "
                f"en ${copper:.2f}/lb y el crecimiento de inversión en infraestructura de IA ({ai_capex:.1f}% YoY). "
                f"Existe también presión secundaria de tipo {second_regime}."
            )
        elif top_regime == "MONETARY_STRESS":
            primary_driver = "Revalorización del oro físico y persistencia de rendimientos soberanos elevados"
            rationale = (
                f"Las condiciones macroeconómicas observadas son consistentes con un régimen de MONETARY_STRESS "
                f"(Nivel de confianza: {int(confidence*100)}%), evidenciado por la demanda de refugio en oro (${gold:.0f}/oz) "
                f"y tasas del Tesoro a 10 años en {us10y:.2f}%."
            )
        elif top_regime == "FISCAL_STRESS":
            primary_driver = "Déficit fiscal estructural en EE.UU. y elevada emisión de bonos de largo plazo"
            rationale = (
                f"Las condiciones macroeconómicas observadas son consistentes con un régimen de FISCAL_STRESS "
                f"(Nivel de confianza: {int(confidence*100)}%), impulsado por un déficit de {deficit:.1f}% del PIB "
                f"y tasa a 30 años en {us30y:.2f}%."
            )
        else:
            primary_driver = "Balance neutral entre inflación controlada y actividad moderada"
            rationale = (
                f"Las condiciones macroeconómicas observadas son consistentes con un régimen de {top_regime} "
                f"(Nivel de confianza: {int(confidence*100)}%), caracterizado por estabilidad en variables clave."
            )

        indicators_state = {
            "copper_usd_lb": copper,
            "gold_usd_oz": gold,
            "us10y_pct": us10y,
            "us30y_pct": us30y,
            "us_cpi_pct": us_cpi,
            "dxy_index": dxy,
            "china_pmi": china_pmi,
            "ai_capex_growth_pct": ai_capex,
            "evaluated_probabilities": {r: round(s/total_score, 3) for r, s in sorted_regimes}
        }

        # Persist regime record
        regime_record = Regime(
            timestamp=datetime.datetime.utcnow(),
            regime_code=top_regime,
            confidence=confidence,
            primary_driver=primary_driver,
            rationale=rationale,
            indicators_state=indicators_state
        )
        self.db.add(regime_record)
        self.db.commit()
        self.db.refresh(regime_record)

        logger.info(f"✅ Active Global Regime: {top_regime} (confidence={confidence})")
        return {
            "id": regime_record.id,
            "regime_code": top_regime,
            "confidence": confidence,
            "primary_driver": primary_driver,
            "rationale": rationale,
            "indicators_state": indicators_state,
            "timestamp": regime_record.timestamp.isoformat()
        }

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
