import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.models import Indicator, Observation, Signal, DerivedIndicator
from packages.common.database import SessionLocal

logger = logging.getLogger(__name__)

class DerivedIndicatorsEngine:
    """
    Computes derived indicators (Yield Curve Spread, Real Rates, Gold/Copper ratio, etc.)
    and detects quantitative signals (Inversions, Z-score shocks, 200MA crossings).
    """

    def __init__(self, db: Optional[Session] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()

    def run(self) -> dict:
        """Execute derived calculations and signal generation."""
        logger.info("⚡ Executing Derived Indicators and Signals Engine...")
        results = {
            "derived_calculated": 0,
            "signals_generated": 0,
            "errors": []
        }

        try:
            # 1. Fetch latest observations by indicator code
            latest_obs = self._get_latest_observations()

            # 2. Compute Yield Spread 10Y - 2Y
            if "US10Y" in latest_obs and "US2Y" in latest_obs:
                us10y = latest_obs["US10Y"].value
                us2y = latest_obs["US2Y"].value
                spread = round(us10y - us2y, 4)
                
                # Signal: Yield Curve Inversion / Normalization
                signal_type = "YIELD_CURVE_INVERTED" if spread < 0 else "YIELD_CURVE_NORMAL"
                self._record_signal(
                    indicator_code="US10Y",
                    signal_type=signal_type,
                    strength=-1.0 if spread < 0 else 0.5,
                    value=spread,
                    baseline=0.0,
                    metadata={"spread_10y_2y": spread, "us10y": us10y, "us2y": us2y}
                )
                results["derived_calculated"] += 1
                results["signals_generated"] += 1

            # 3. Compute Gold / Copper Ratio
            if "GOLD" in latest_obs and "COPPER" in latest_obs:
                gold = latest_obs["GOLD"].value
                copper = latest_obs["COPPER"].value
                if copper > 0:
                    ratio = round(gold / (copper * 100), 4)  # (USD/oz) / (USD/lb * 100)
                    self._record_signal(
                        indicator_code="COPPER",
                        signal_type="GOLD_COPPER_RATIO_EVAL",
                        strength=1.0 if ratio < 5.5 else -0.8,
                        value=ratio,
                        baseline=5.5,
                        metadata={"gold_price": gold, "copper_price": copper, "ratio": ratio}
                    )
                    results["derived_calculated"] += 1
                    results["signals_generated"] += 1

            # 4. Compute Real Rate (US10Y - US_CPI)
            if "US10Y" in latest_obs and "US_CPI" in latest_obs:
                us10y = latest_obs["US10Y"].value
                cpi = latest_obs["US_CPI"].value
                real_rate = round(us10y - cpi, 3)
                self._record_signal(
                    indicator_code="US10Y",
                    signal_type="REAL_RATE_TIGHTENING" if real_rate > 1.5 else "REAL_RATE_ACCOMMODATIVE",
                    strength=real_rate / 2.0,
                    value=real_rate,
                    baseline=1.0,
                    metadata={"real_rate_10y": real_rate, "us10y": us10y, "us_cpi": cpi}
                )
                results["derived_calculated"] += 1
                results["signals_generated"] += 1

            self.db.commit()
            logger.info(f"✅ Derived indicators updated: {results}")

        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error in DerivedIndicatorsEngine: {e}", exc_info=True)
            results["errors"].append(str(e))

        return results

    def _get_latest_observations(self) -> dict[str, Observation]:
        """Retrieve most recent observation for each registered indicator."""
        indicators = self.db.query(Indicator).all()
        latest_map = {}
        for ind in indicators:
            latest = self.db.query(Observation).filter(
                Observation.indicator_id == ind.id
            ).order_by(Observation.timestamp.desc()).first()
            if latest:
                latest_map[ind.code] = latest
        return latest_map

    def _record_signal(
        self, 
        indicator_code: str, 
        signal_type: str, 
        strength: float, 
        value: float, 
        baseline: float, 
        metadata: dict
    ):
        indicator = self.db.query(Indicator).filter(Indicator.code == indicator_code).first()
        if not indicator:
            return

        signal = Signal(
            indicator_id=indicator.id,
            timestamp=datetime.datetime.utcnow(),
            signal_type=signal_type,
            signal_strength=strength,
            value=value,
            baseline=baseline,
            metadata_json=metadata
        )
        self.db.add(signal)

    def close(self):
        if not self.db_provided:
            self.db.close()
