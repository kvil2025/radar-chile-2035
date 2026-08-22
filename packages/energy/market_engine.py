import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from packages.common.models import Bus, NodePrice

class EnergyMarketEngine:
    """
    Calculates capture prices, capture rates, BESS arbitrage spreads,
    and curtailment risks across all SEN electrical buses.
    """

    def __init__(self, db: Session):
        self.db = db

    def calculate_bus_market_metrics(self, bus_id: int) -> Dict[str, float]:
        """Compute average price, solar capture price, wind capture price, and BESS spread for a bus."""
        prices = self.db.query(NodePrice).filter(NodePrice.bus_id == bus_id).order_by(NodePrice.timestamp.asc()).all()
        if not prices:
            return {
                "avg_price_usd_mwh": 50.0,
                "solar_capture_price": 25.0,
                "wind_capture_price": 48.0,
                "bess_arbitrage_spread": 60.0,
                "price_volatility": 15.0,
                "zero_price_hours_pct": 10.0
            }

        df = pd.DataFrame([
            {
                "timestamp": p.timestamp,
                "hour": p.timestamp.hour,
                "price": p.price_usd_mwh
            }
            for p in prices
        ])

        avg_price = float(df["price"].mean())
        volatility = float(df["price"].std()) if len(df) > 1 else 0.0
        zero_hours = float((df["price"] <= 1.0).mean() * 100.0)

        # Solar profile weight: peak at 13:00 (hours 9 to 17)
        solar_weights = df["hour"].apply(lambda h: max(0.0, 1.0 - ((h - 13) / 5.0) ** 2) if 8 <= h <= 18 else 0.0)
        solar_capture = float((df["price"] * solar_weights).sum() / (solar_weights.sum() + 1e-6))

        # Wind profile weight: higher afternoon & night (hours 17 to 6)
        wind_weights = df["hour"].apply(lambda h: 1.0 if (h >= 17 or h <= 6) else 0.4)
        wind_capture = float((df["price"] * wind_weights).sum() / (wind_weights.sum() + 1e-6))

        # BESS Arbitrage: Average price in peak discharge hours (19 to 23) minus lowest charge hours (11 to 15)
        peak_discharge_price = float(df[df["hour"].isin([19, 20, 21, 22, 23])]["price"].mean()) if not df[df["hour"].isin([19, 20, 21, 22, 23])].empty else avg_price * 1.5
        day_charge_price = float(df[df["hour"].isin([11, 12, 13, 14, 15])]["price"].mean()) if not df[df["hour"].isin([11, 12, 13, 14, 15])].empty else avg_price * 0.3
        bess_spread = max(0.0, (peak_discharge_price * 0.85) - day_charge_price)

        return {
            "avg_price_usd_mwh": round(avg_price, 2),
            "solar_capture_price": round(solar_capture, 2),
            "wind_capture_price": round(wind_capture, 2),
            "bess_arbitrage_spread": round(bess_spread, 2),
            "price_volatility": round(volatility, 2),
            "zero_price_hours_pct": round(zero_hours, 1)
        }
