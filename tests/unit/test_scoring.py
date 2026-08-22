from packages.scoring.normalizers import normalize_min_max, normalize_z_score_sigmoid
from packages.scoring.engine import ScoringEngine

def test_normalize_min_max_direction_positive():
    # Value in middle
    assert normalize_min_max(50.0, 0.0, 100.0, direction=1) == 50.0
    # Value at max
    assert normalize_min_max(100.0, 0.0, 100.0, direction=1) == 100.0
    # Value at min
    assert normalize_min_max(0.0, 0.0, 100.0, direction=1) == 0.0

def test_normalize_min_max_direction_negative():
    # When direction = -1, higher raw value means lower score
    assert normalize_min_max(100.0, 0.0, 100.0, direction=-1) == 0.0
    assert normalize_min_max(0.0, 0.0, 100.0, direction=-1) == 100.0

def test_scoring_engine_contributors_sum(db_session):
    engine = ScoringEngine(db=db_session)
    scores = engine.run_all()
    
    assert len(scores) == 5
    assert "CHILE_OPPORTUNITY" in scores
    assert "MINING_CYCLE" in scores
    assert "COMMODITY_CYCLE" in scores
    assert "MONETARY_STRESS" in scores
    assert "DOLLAR_STRESS" in scores

    for s_type, val in scores.items():
        assert 0.0 <= val <= 100.0
