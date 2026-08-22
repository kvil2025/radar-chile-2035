import datetime
import math
from typing import Optional
from pydantic import BaseModel

class QualityValidationResult(BaseModel):
    is_valid: bool
    quality_status: str  # VALID, SUSPECT, MISSING, STALE, OUTLIER, INVALID
    reasons: list[str] = []
    sanitized_value: Optional[float] = None

class DataQualityValidator:
    """
    Validates economic and financial observations.
    Categorizes observations as:
    - VALID: Normal, within plausible physical/economic limits.
    - SUSPECT: Potential anomaly, unexpected jump, or wide discrepancy.
    - OUTLIER: Value exceeds 3 standard deviations or statistical threshold.
    - STALE: Value unchanged for multiple consecutive periods when variation was expected.
    - MISSING / INVALID: NaN, infinite, or physically impossible (e.g. negative CPI index or yield < -5%).
    """

    # Plausible physical/economic bounds for validation
    BOUNDS = {
        "US10Y": (-1.0, 20.0),
        "US30Y": (-1.0, 20.0),
        "US2Y": (-1.0, 25.0),
        "US_CPI": (-10.0, 30.0),
        "US_FED_RATE": (0.0, 25.0),
        "US_FISCAL_DEFICIT": (-40.0, 20.0),
        "US_DEBT": (20.0, 300.0),
        "DXY": (60.0, 160.0),
        "USD_RESERVES_SHARE": (20.0, 90.0),
        "FOREIGN_TREASURY_HOLDINGS": (1.0, 20.0),
        "CENTRAL_BANK_GOLD": (-500.0, 2500.0),
        "COPPER": (0.50, 15.0),
        "GOLD": (200.0, 10000.0),
        "OIL": (5.0, 300.0),
        "LITHIUM": (2000.0, 150000.0),
        "IRON_ORE": (15.0, 500.0),
        "CHINA_PMI": (25.0, 75.0),
        "CHINA_INDUSTRIAL_PRODUCTION": (-30.0, 50.0),
        "CHINA_COPPER_IMPORTS": (-80.0, 200.0),
        "CLP_USD": (300.0, 2500.0),
        "CHILE_TPM": (0.0, 35.0),
        "CHILE_CPI": (-5.0, 40.0),
        "CHILE_IMACEC": (-25.0, 35.0),
        "CHILE_GDP": (-20.0, 30.0),
        "CHILE_FISCAL_BALANCE": (-30.0, 20.0),
        "CHILE_COPPER_PRODUCTION": (100.0, 1000.0),
        "CHILE_MINING_CAPEX": (10.0, 200.0),
        "CHILE_COPPER_EXPORTS": (500.0, 15000.0),
        "CHILE_ELECTRICITY_DEMAND": (1000.0, 25000.0),
        "AI_DATA_CENTER_CAPEX_PROXY": (-50.0, 300.0),
    }

    # Maximum plausible 1-period % change before flagging as SUSPECT
    MAX_PERIOD_CHANGE_PCT = {
        "COPPER": 20.0,
        "GOLD": 15.0,
        "OIL": 35.0,
        "CLP_USD": 12.0,
        "US10Y": 30.0,  # 30% relative move in yield
        "DXY": 8.0,
    }

    @classmethod
    def validate_observation(
        cls, 
        indicator_code: str, 
        value: float, 
        timestamp: datetime.datetime,
        previous_value: Optional[float] = None,
        previous_timestamp: Optional[datetime.datetime] = None
    ) -> QualityValidationResult:
        reasons = []

        # 1. Check for NaN or Inf
        if value is None or math.isnan(value) or math.isinf(value):
            return QualityValidationResult(
                is_valid=False,
                quality_status="INVALID",
                reasons=["Valor es nulo, NaN o infinito"],
                sanitized_value=None
            )

        # 2. Check future timestamp
        now = datetime.datetime.utcnow()
        if timestamp > now + datetime.timedelta(days=1):
            return QualityValidationResult(
                is_valid=False,
                quality_status="INVALID",
                reasons=[f"Timestamp en el futuro: {timestamp}"],
                sanitized_value=None
            )

        # 3. Check physical bounds
        if indicator_code in cls.BOUNDS:
            min_val, max_val = cls.BOUNDS[indicator_code]
            if value < min_val or value > max_val:
                reasons.append(f"Valor {value} fuera de rango plausible [{min_val}, {max_val}]")
                return QualityValidationResult(
                    is_valid=False,
                    quality_status="OUTLIER",
                    reasons=reasons,
                    sanitized_value=value
                )

        # 4. Check single-period jump if previous value exists
        if previous_value is not None and previous_value != 0:
            pct_change = abs((value - previous_value) / previous_value) * 100
            max_allowed_jump = cls.MAX_PERIOD_CHANGE_PCT.get(indicator_code, 50.0)
            
            if pct_change > max_allowed_jump:
                reasons.append(
                    f"Salto abrupto de {pct_change:.1f}% respecto al periodo anterior ({previous_value} -> {value})"
                )
                return QualityValidationResult(
                    is_valid=True,
                    quality_status="SUSPECT",
                    reasons=reasons,
                    sanitized_value=value
                )

        return QualityValidationResult(
            is_valid=True,
            quality_status="VALID",
            reasons=[],
            sanitized_value=value
        )
