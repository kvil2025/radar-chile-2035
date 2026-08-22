import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.models import TransmissionChannel, Indicator, Observation
from packages.common.database import SessionLocal

logger = logging.getLogger(__name__)

class ChileImpactEngine:
    """
    Evaluates global macroeconomic transmission channels into Chilean domestic variables
    (e.g., US Rates -> CLP, Copper -> Fiscal Revenue, China PMI -> Mining Exports, AI Capex -> SEN Energy).
    """

    def __init__(self, db: Optional[Session] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()

    def evaluate_channels(self) -> dict:
        """Calculate dynamic transmission impact scores for all active channels."""
        logger.info("🇨🇱 Evaluating Chile Transmission Channels...")
        latest_obs = self._get_latest_observations()

        channels = self.db.query(TransmissionChannel).all()
        channel_results = []
        positive_impacts = []
        negative_impacts = []

        copper = latest_obs.get("COPPER", 4.35)
        us10y = latest_obs.get("US10Y", 4.25)
        china_pmi = latest_obs.get("CHINA_PMI", 50.8)
        ai_capex = latest_obs.get("AI_DATA_CENTER_CAPEX_PROXY", 34.0)

        for ch in channels:
            impact_score = 0.0

            if ch.global_indicator_code == "US10Y":
                # Higher US10Y tightens local financial conditions
                # Baseline 4.0% -> for each 0.10% over baseline, -10 points
                deviation = us10y - 4.0
                impact_score = round(-deviation * 60.0 * ch.elasticity, 1)

            elif ch.global_indicator_code == "COPPER":
                # Baseline $4.00/lb -> for each $0.10 over baseline, +12 points
                deviation = copper - 4.00
                impact_score = round(deviation * 100.0 * ch.elasticity, 1)

            elif ch.global_indicator_code == "CHINA_PMI":
                # Baseline 50.0 -> for each 1.0 point above, +15 points
                deviation = china_pmi - 50.0
                impact_score = round(deviation * 25.0 * ch.elasticity, 1)

            elif ch.global_indicator_code == "AI_DATA_CENTER_CAPEX_PROXY":
                # Baseline 20% YoY -> for each 5% over baseline, +6 points
                deviation = (ai_capex - 20.0) / 5.0
                impact_score = round(deviation * 8.0 * ch.elasticity, 1)

            ch.current_impact_score = max(-100.0, min(100.0, impact_score))
            ch.updated_at = datetime.datetime.utcnow()
            self.db.add(ch)

            channel_dict = {
                "id": ch.id,
                "channel_name": ch.channel_name,
                "global_indicator_code": ch.global_indicator_code,
                "chile_indicator_code": ch.chile_indicator_code,
                "transmission_speed": ch.transmission_speed,
                "elasticity": ch.elasticity,
                "description": ch.description,
                "current_impact_score": ch.current_impact_score,
                "updated_at": ch.updated_at.isoformat()
            }
            channel_results.append(channel_dict)

            if impact_score > 0:
                positive_impacts.append((ch.channel_name, impact_score))
            else:
                negative_impacts.append((ch.channel_name, impact_score))

        self.db.commit()

        # Calculate Net Chile Opportunity Score (-100 to +100)
        net_score = round(sum(ch["current_impact_score"] for ch in channel_results) / max(1, len(channel_results)), 1)
        best_channel = max(channel_results, key=lambda x: x["current_impact_score"])["channel_name"] if channel_results else "N/A"
        worst_channel = min(channel_results, key=lambda x: x["current_impact_score"])["channel_name"] if channel_results else "N/A"

        logger.info(f"✅ Chile Impact Evaluation completed. Net Score: {net_score}")
        return {
            "net_opportunity_score": net_score,
            "primary_positive_channel": best_channel,
            "primary_risk_channel": worst_channel,
            "channels": channel_results
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
