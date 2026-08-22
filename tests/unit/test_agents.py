from packages.agents.chief_economist import ChiefEconomistAgent
from packages.agents.stress_testing import StressTestingAgent

def test_chief_economist_briefing(db_session):
    agent = ChiefEconomistAgent(db=db_session)
    briefing = agent.generate_executive_briefing()
    
    assert "title" in briefing
    assert "content" in briefing
    assert len(briefing["content"]) > 100
    assert "WHAT" in briefing["content"].upper()
    assert "SO WHAT" in briefing["content"].upper()

def test_chief_economist_question(db_session):
    agent = ChiefEconomistAgent(db=db_session)
    res = agent.answer_macro_question("¿Por qué el precio del cobre impacta el balance fiscal de Chile?")
    
    assert "answer" in res
    assert len(res["answer"]) > 50

def test_stress_testing_positive_copper_shock(db_session):
    agent = StressTestingAgent(db=db_session)
    res = agent.simulate_shock(
        copper_price=5.20,  # +$0.82/lb over baseline
        us10y_yield=4.00,
        oil_price=75.0,
        china_pmi=52.0,
        dxy_index=102.0
    )
    
    projections = res["projections"]
    assert projections["fiscal_impact_usd_million"] > 0
    assert projections["projected_clp_usd"] < 932.50  # CLP appreciates
    assert projections["simulated_chile_opportunity_score"] > 55.0
    assert projections["simulated_regime"] in ["COMMODITY_SUPERCYCLE", "EXPANSION"]
    assert "ai_assessment" in res

def test_stress_testing_negative_shock(db_session):
    agent = StressTestingAgent(db=db_session)
    res = agent.simulate_shock(
        copper_price=3.40,  # -$0.98/lb under baseline
        us10y_yield=5.60,   # High yield stress
        oil_price=95.0,
        china_pmi=47.0,
        dxy_index=110.0
    )
    
    projections = res["projections"]
    assert projections["fiscal_impact_usd_million"] < 0
    assert projections["projected_clp_usd"] > 950.0  # CLP depreciates
    assert projections["simulated_dollar_stress_score"] > 60.0
    assert projections["simulated_regime"] in ["RECESSION", "MONETARY_STRESS"]
