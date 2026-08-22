def test_costo_marginal_dataset_summary_endpoint(client):
    res = client.get("/api/v1/costo-marginal/dataset-summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_records" in data
    assert data["total_records"] > 0

def test_costo_marginal_train_predict_endpoint(client):
    res = client.post("/api/v1/costo-marginal/train-predict?horizon_hours=24&n_estimators=20")
    assert res.status_code == 200
    data = res.json()
    assert "forecast" in data
    assert len(data["forecast"]) == 24
    assert "feature_importance" in data

def test_costo_marginal_climate_correlation_endpoint(client):
    res = client.get("/api/v1/costo-marginal/climate-correlation")
    assert res.status_code == 200
    data = res.json()
    assert "correlation_matrix" in data

def test_costo_marginal_regulatory_corpus_endpoint(client):
    res = client.get("/api/v1/costo-marginal/regulatory-corpus?query=PMGD")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
