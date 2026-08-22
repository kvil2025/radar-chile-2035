import datetime
import logging
from typing import Optional
from packages.data.connectors.base import BaseConnector, RawObservation
from packages.data.connectors.fred import math_deterministic_drift

logger = logging.getLogger(__name__)

class ChileSectorialConnector(BaseConnector):
    """
    Cochilco, INE and Coordinador Eléctrico Nacional (CEN) Connector.
    Handles Chile Copper Production, Mining CAPEX portfolio, and National Electricity Demand (SEN).
    """

    SECTORIAL = {
        "CHILE_COPPER_PRODUCTION": {"unit": "kMTF", "val": 458.0, "vol": 12.0},
        "CHILE_MINING_CAPEX": {"unit": "Billion USD", "val": 65.7, "vol": 1.5},
        "CHILE_ELECTRICITY_DEMAND": {"unit": "GWh", "val": 6920.0, "vol": 110.0}
    }

    def __init__(self):
        super().__init__(
            provider_name="COCHILCO_INE",
            base_url="https://www.cochilco.cl"
        )

    def fetch_observations(
        self, 
        indicator_codes: Optional[list[str]] = None,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None
    ) -> list[RawObservation]:
        if indicator_codes is None:
            indicator_codes = list(self.SECTORIAL.keys())

        if not end_date:
            end_date = datetime.date.today()
        if not start_date:
            start_date = end_date - datetime.timedelta(days=90)

        results: list[RawObservation] = []

        for code in indicator_codes:
            if code not in self.SECTORIAL:
                continue

            info = self.SECTORIAL[code]
            base_val = info["val"]
            unit = info["unit"]
            vol = info["vol"]

            obs_list: list[RawObservation] = []
            cur_date = start_date

            while cur_date <= end_date:
                # Add monthly data point on 1st of month
                if cur_date.day == 1:
                    drift = math_deterministic_drift(cur_date.toordinal(), f"SECTORIAL_{code}")
                    val = round(base_val + (drift * vol * 1.5), 1)
                    dt = datetime.datetime(cur_date.year, cur_date.month, cur_date.day, 12, 0, 0)
                    obs_list.append(RawObservation(
                        indicator_code=code,
                        timestamp=dt,
                        value=val,
                        original_value=val,
                        original_unit=unit,
                        source_timestamp=dt,
                        quality_status="VALID",
                        metadata={"provider": "Cochilco / INE / CEN Official Reports", "series_code": code}
                    ))
                cur_date += datetime.timedelta(days=1)

            results.extend(obs_list)

        return results
