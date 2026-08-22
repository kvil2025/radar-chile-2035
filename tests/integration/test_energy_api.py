def test_get_energy_buses(client):
    res = client.get("/api/v1/energy/buses")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 20
    assert any(b["code"] == "KIMAL_500" for b in data)

def test_get_substations_and_lines(client):
    res_subs = client.get("/api/v1/energy/substations")
    assert res_subs.status_code == 200
    assert len(res_subs.json()) >= 15

    res_lines = client.get("/api/v1/energy/lines")
    assert res_lines.status_code == 200
    assert len(res_lines.json()) >= 10

def test_get_generation_and_demand_mix(client):
    res_gen = client.get("/api/v1/energy/generation-mix")
    assert res_gen.status_code == 200
    data_gen = res_gen.json()
    assert len(data_gen) > 0
    assert "solar_mw" in data_gen[0]
    assert "renewable_share_pct" in data_gen[0]

    res_dem = client.get("/api/v1/energy/demand-hourly")
    assert res_dem.status_code == 200
    data_dem = res_dem.json()
    assert len(data_dem) > 0
    assert "mining_demand_mw" in data_dem[0]

def test_get_projects_pipeline(client):
    res = client.get("/api/v1/energy/projects")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 5
    assert any("BESS" in p["technology"] or "SOLAR" in p["technology"] for p in data)

def test_node_opportunity_ranking_endpoint(client):
    res = client.get("/api/v1/energy/node-opportunity-ranking")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 20
    assert data[0]["total_score"] >= data[-1]["total_score"]

def test_project_analyzer_endpoint(client):
    payload = {
        "technology": "SOLAR_PLUS_BESS",
        "capacity_mw": 100.0,
        "storage_mwh": 400.0,
        "target_cod_year": 2029,
        "lifetime_years": 25,
        "discount_rate_pct": 8.0
    }
    res = client.post("/api/v1/energy/project-analyzer", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "top_buses_ranking" in data
    assert len(data["top_buses_ranking"]) == 10
    assert data["top_buses_ranking"][0]["rank"] == 1

def test_export_excel_endpoint(client):
    payload = {
        "technology": "SOLAR_PLUS_BESS",
        "capacity_mw": 100.0,
        "storage_mwh": 400.0,
        "target_cod_year": 2029,
        "lifetime_years": 25,
        "discount_rate_pct": 8.0
    }
    res = client.post("/api/v1/energy/export/excel", json=payload)
    assert res.status_code == 200
    assert "application/vnd.ms-excel" in res.headers["content-type"]
    assert len(res.content) > 500
    assert b"Resumen Ejecutivo" in res.content

def test_export_memo_html_endpoint(client):
    payload = {
        "technology": "SOLAR_PLUS_BESS",
        "capacity_mw": 100.0,
        "storage_mwh": 400.0,
        "target_cod_year": 2029,
        "lifetime_years": 25,
        "discount_rate_pct": 8.0
    }
    res = client.post("/api/v1/energy/export/memo-html", json=payload)
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert b"MEMOR\xc3\x81NDUM DE INVERSI\xc3\x93N" in res.content or b"MEMORANDUM" in res.content or b"RADAR CHILE" in res.content
