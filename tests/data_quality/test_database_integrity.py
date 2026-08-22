from sqlalchemy import func
from packages.common.models import Indicator, Observation, Source

def test_no_duplicate_indicator_timestamps(db_session):
    """Ensure no duplicate observation timestamps exist for any single indicator."""
    duplicates = db_session.query(
        Observation.indicator_id,
        Observation.timestamp,
        func.count(Observation.id)
    ).group_by(
        Observation.indicator_id,
        Observation.timestamp
    ).having(func.count(Observation.id) > 1).all()

    assert len(duplicates) == 0, f"Found {len(duplicates)} duplicate observation timestamps in database."

def test_all_master_indicators_have_observations(db_session):
    """Ensure every master indicator registered has at least 1 validated historical observation."""
    indicators = db_session.query(Indicator).all()
    assert len(indicators) == 30

    for ind in indicators:
        count = db_session.query(Observation).filter(Observation.indicator_id == ind.id).count()
        assert count > 0, f"Indicator {ind.code} has 0 observations."

def test_observation_quality_status_tags(db_session):
    """Ensure all observations possess a legitimate quality status."""
    valid_statuses = {"VALID", "SUSPECT", "MISSING", "STALE", "OUTLIER", "INVALID"}
    invalid_tags = db_session.query(Observation).filter(
        ~Observation.quality_status.in_(valid_statuses)
    ).all()
    assert len(invalid_tags) == 0
