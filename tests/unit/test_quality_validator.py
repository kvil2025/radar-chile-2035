import datetime
from packages.data.quality.validator import DataQualityValidator

def test_validate_valid_observation():
    res = DataQualityValidator.validate_observation(
        indicator_code="COPPER",
        value=4.42,
        timestamp=datetime.datetime.utcnow()
    )
    assert res.is_valid is True
    assert res.quality_status == "VALID"
    assert len(res.reasons) == 0

def test_validate_out_of_bounds_outlier():
    res = DataQualityValidator.validate_observation(
        indicator_code="COPPER",
        value=25.0,  # Physically absurd copper price
        timestamp=datetime.datetime.utcnow()
    )
    assert res.is_valid is False
    assert res.quality_status == "OUTLIER"
    assert "fuera de rango plausible" in res.reasons[0]

def test_validate_nan_or_inf():
    res = DataQualityValidator.validate_observation(
        indicator_code="US10Y",
        value=float("nan"),
        timestamp=datetime.datetime.utcnow()
    )
    assert res.is_valid is False
    assert res.quality_status == "INVALID"

def test_validate_abrupt_jump():
    res = DataQualityValidator.validate_observation(
        indicator_code="COPPER",
        value=4.20,
        timestamp=datetime.datetime.utcnow(),
        previous_value=2.50  # 68% single-period jump
    )
    assert res.is_valid is True
    assert res.quality_status == "SUSPECT"
    assert "Salto abrupto" in res.reasons[0]
