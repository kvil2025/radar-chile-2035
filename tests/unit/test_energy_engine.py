from packages.common.models import Bus
from packages.common.schemas import ProjectEvaluationRequest
from packages.energy.market_engine import EnergyMarketEngine
from packages.energy.node_scoring import NodeScoringEngine
from packages.energy.project_evaluator import ProjectEvaluator

def test_market_engine_metrics(db_session):
    bus = db_session.query(Bus).filter(Bus.code == "KIMAL_500").first()
    assert bus is not None
    
    engine = EnergyMarketEngine(db=db_session)
    metrics = engine.calculate_bus_market_metrics(bus.id)
    
    assert "avg_price_usd_mwh" in metrics
    assert "solar_capture_price" in metrics
    assert "bess_arbitrage_spread" in metrics
    assert metrics["bess_arbitrage_spread"] > 0

def test_node_scoring_all_buses(db_session):
    engine = NodeScoringEngine(db=db_session)
    scores = engine.calculate_all_scores()
    
    assert len(scores) >= 20
    for s in scores:
        assert 0.0 <= s.total_score <= 100.0
        assert s.recommendation_level in ["HIGHLY_ATTRACTIVE", "ATTRACTIVE", "MODERATE", "RISKY", "AVOID"]

def test_project_evaluator_solar_plus_bess(db_session):
    evaluator = ProjectEvaluator(db=db_session)
    req = ProjectEvaluationRequest(
        technology="SOLAR_PLUS_BESS",
        capacity_mw=100.0,
        storage_mwh=400.0,
        target_cod_year=2029,
        lifetime_years=25,
        discount_rate_pct=8.0
    )
    res = evaluator.evaluate_project(req)
    
    assert res.estimated_capex_musd > 100.0  # ~168M USD for 100MW PV + 400MWh BESS
    assert len(res.top_buses_ranking) == 10
    top_bus = res.top_buses_ranking[0]
    assert top_bus.rank == 1
    assert top_bus.npv_musd is not None
    assert top_bus.irr_pct > 5.0
    assert top_bus.payback_years < 25.0
    assert len(top_bus.summary_rationale) > 20

def test_project_evaluator_wind_project(db_session):
    evaluator = ProjectEvaluator(db=db_session)
    req = ProjectEvaluationRequest(
        technology="WIND",
        capacity_mw=150.0,
        storage_mwh=0.0,
        target_cod_year=2028,
        lifetime_years=25
    )
    res = evaluator.evaluate_project(req)
    assert len(res.top_buses_ranking) == 10
    for b in res.top_buses_ranking:
        assert b.lcoe_usd_mwh > 0
