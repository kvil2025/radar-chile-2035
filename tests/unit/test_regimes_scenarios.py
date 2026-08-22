from packages.scenarios.regimes import EconomicRegimeClassifier
from packages.scenarios.scenario_engine import ScenarioEngine
from packages.scenarios.chile_impact import ChileImpactEngine

def test_economic_regime_classification(db_session):
    classifier = EconomicRegimeClassifier(db=db_session)
    regime = classifier.classify()
    
    assert regime["regime_code"] in EconomicRegimeClassifier.REGIMES
    assert 0.0 <= regime["confidence"] <= 1.0
    assert "Las condiciones macroeconómicas observadas son consistentes con" in regime["rationale"]

def test_scenarios_evaluation(db_session):
    engine = ScenarioEngine(db=db_session)
    scenarios = engine.evaluate_scenarios()
    
    assert len(scenarios) == 4
    total_prob = sum(s["probability"] for s in scenarios)
    assert 0.99 <= total_prob <= 1.01  # Sums to ~1.0
    
    for s in scenarios:
        assert s["probability_type"] == "MODEL_ESTIMATE"
        assert s["expected_chile_effect"] is not None

def test_chile_impact_channels(db_session):
    chile_engine = ChileImpactEngine(db=db_session)
    res = chile_engine.evaluate_channels()
    
    assert "net_opportunity_score" in res
    assert len(res["channels"]) >= 4
    assert res["primary_positive_channel"] != ""
