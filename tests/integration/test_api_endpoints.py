def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "operational"
    assert data["database"] == "healthy"

def test_list_sources(client):
    res = client.get("/api/v1/sources")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 5
    providers = [s["provider"] for s in data]
    assert "FRED" in providers
    assert "BANCO_CENTRAL_CHILE" in providers

def test_list_indicators(client):
    res = client.get("/api/v1/indicators")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 30
    codes = [i["code"] for i in data]
    assert "COPPER" in codes
    assert "US10Y" in codes
    assert "CLP_USD" in codes

def test_get_observations_series(client):
    res = client.get("/api/v1/observations/COPPER?limit=10")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert "value" in data[0]
    assert "quality_status" in data[0]

def test_get_scores(client):
    res = client.get("/api/v1/scores")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 5
    first = data[0]
    assert "contributors" in first
    assert "confidence" in first
    assert "methodology_version" in first

def test_get_regime(client):
    res = client.get("/api/v1/regime")
    assert res.status_code == 200
    data = res.json()
    assert "regime_code" in data
    assert "rationale" in data

def test_get_scenarios(client):
    res = client.get("/api/v1/scenarios")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 4
    for sc in data:
        assert sc["probability_type"] == "MODEL_ESTIMATE"

def test_get_chile_impact(client):
    res = client.get("/api/v1/chile-impact")
    assert res.status_code == 200
    data = res.json()
    assert "net_opportunity_score" in data
    assert "channels" in data

def test_get_alerts(client):
    res = client.get("/api/v1/alerts")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
