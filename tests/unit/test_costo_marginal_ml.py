from packages.costo_marginal.ml_forecast_engine import MLForecastEngine
from packages.costo_marginal.climate_analytics import ClimateAnalyticsEngine
from packages.costo_marginal.regulatory_corpus import RegulatoryCorpusEngine

def test_ml_forecast_engine_summary():
    engine = MLForecastEngine()
    summary = engine.get_dataset_summary()
    assert "total_records" in summary
    assert summary["total_records"] > 1000
    assert "metrics" in summary
    assert summary["metrics"]["avg_cost_usd_mwh"] > 0

def test_ml_forecast_training_and_prediction():
    engine = MLForecastEngine()
    res = engine.train_and_forecast(forecast_horizon_hours=24, n_estimators=20)
    
    assert "metrics" in res
    assert res["metrics"]["r2_score"] is not None
    assert "forecast" in res
    assert len(res["forecast"]) == 24
    
    first_pt = res["forecast"][0]
    assert "predicted_cost_usd_mwh" in first_pt
    assert "upper_bound_95" in first_pt
    assert first_pt["upper_bound_95"] >= first_pt["predicted_cost_usd_mwh"]
    assert "feature_importance" in res

def test_climate_analytics_correlations():
    engine = ClimateAnalyticsEngine()
    corr = engine.compute_climate_correlations()
    assert "correlation_matrix" in corr
    assert "temperature_sensitivity" in corr
    assert "hourly_profile" in corr
    assert len(corr["hourly_profile"]) == 24

def test_regulatory_corpus_search():
    docs = RegulatoryCorpusEngine.get_all_documents()
    assert len(docs) >= 4
    
    search_bess = RegulatoryCorpusEngine.search_documents(query="Almacenamiento")
    assert len(search_bess) >= 1
    assert any(d["id"] == "REG-LEY21505" for d in search_bess)
