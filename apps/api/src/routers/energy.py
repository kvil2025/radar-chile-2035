from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from packages.common.models import (
    Bus, Substation, TransmissionLine, GenerationPlant, BessUnit,
    ProjectPipeline, NodePrice, GenerationHourly, DemandHourly,
    FuelPrice, HydroBasin, NodeOpportunityScore
)
from packages.common.schemas import (
    BusResponse, SubstationResponse, TransmissionLineResponse,
    GenerationPlantResponse, BessUnitResponse, ProjectPipelineResponse,
    NodePriceResponse, GenerationHourlyResponse, DemandHourlyResponse,
    FuelPriceResponse, HydroBasinResponse, NodeOpportunityScoreResponse,
    ProjectEvaluationRequest, ProjectEvaluationResult
)
from packages.energy.node_scoring import NodeScoringEngine
from packages.energy.project_evaluator import ProjectEvaluator
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/energy", tags=["Energy Intelligence & SEN 2035"])

@router.get("/buses", response_model=List[BusResponse])
def get_buses(zone: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve all SEN electrical buses with their coordinates, zone, and latest opportunity score."""
    query = db.query(Bus)
    if zone:
        query = query.filter(Bus.zone == zone)
    buses = query.all()

    results = []
    for b in buses:
        latest_price_rec = db.query(NodePrice).filter(NodePrice.bus_id == b.id).order_by(NodePrice.timestamp.desc()).first()
        opp_score_rec = db.query(NodeOpportunityScore).filter(NodeOpportunityScore.bus_id == b.id).order_by(NodeOpportunityScore.timestamp.desc()).first()

        results.append(BusResponse(
            id=b.id,
            code=b.code,
            name=b.name,
            voltage_kv=b.voltage_kv,
            latitude=b.latitude,
            longitude=b.longitude,
            zone=b.zone,
            region=b.region,
            substation_id=b.substation_id,
            status=b.status,
            latest_price=latest_price_rec.price_usd_mwh if latest_price_rec else None,
            opportunity_score=opp_score_rec.total_score if opp_score_rec else None,
            recommendation_level=opp_score_rec.recommendation_level if opp_score_rec else None
        ))
    return results

@router.get("/substations", response_model=List[SubstationResponse])
def get_substations(db: Session = Depends(get_db)):
    """Retrieve all SEN substations with their voltage levels and capacity."""
    return db.query(Substation).all()

@router.get("/lines", response_model=List[TransmissionLineResponse])
def get_transmission_lines(db: Session = Depends(get_db)):
    """Retrieve all SEN transmission lines with capacity and utilization."""
    lines = db.query(TransmissionLine).all()
    results = []
    for l in lines:
        results.append(TransmissionLineResponse(
            id=l.id,
            code=l.code,
            name=l.name,
            from_bus_id=l.from_bus_id,
            to_bus_id=l.to_bus_id,
            voltage_kv=l.voltage_kv,
            capacity_mw=l.capacity_mw,
            length_km=l.length_km,
            impedance_ohm=l.impedance_ohm,
            status=l.status,
            from_bus_name=l.from_bus.name if l.from_bus else None,
            to_bus_name=l.to_bus.name if l.to_bus else None,
            current_flow_mw=round(l.capacity_mw * 0.65, 1),
            utilization_pct=65.0,
            is_congested=False
        ))
    return results

@router.get("/plants", response_model=List[GenerationPlantResponse])
def get_generation_plants(technology: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve all operational generation plants in the SEN."""
    query = db.query(GenerationPlant)
    if technology:
        query = query.filter(GenerationPlant.technology == technology)
    plants = query.all()
    results = []
    for p in plants:
        results.append(GenerationPlantResponse(
            id=p.id,
            name=p.name,
            technology=p.technology,
            capacity_mw=p.capacity_mw,
            latitude=p.latitude,
            longitude=p.longitude,
            bus_id=p.bus_id,
            operator=p.operator,
            status=p.status,
            capacity_factor_avg=p.capacity_factor_avg,
            bus_name=p.bus.name if p.bus else None
        ))
    return results

@router.get("/bess", response_model=List[BessUnitResponse])
def get_bess_units(db: Session = Depends(get_db)):
    """Retrieve all BESS battery storage units in the SEN."""
    units = db.query(BessUnit).all()
    results = []
    for u in units:
        results.append(BessUnitResponse(
            id=u.id,
            name=u.name,
            power_mw=u.power_mw,
            energy_mwh=u.energy_mwh,
            duration_hours=u.duration_hours,
            round_trip_efficiency=u.round_trip_efficiency,
            latitude=u.latitude,
            longitude=u.longitude,
            bus_id=u.bus_id,
            operator=u.operator,
            status=u.status,
            bus_name=u.bus.name if u.bus else None
        ))
    return results

@router.get("/projects", response_model=List[ProjectPipelineResponse])
def get_projects_pipeline(status: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve pipeline of future generation, storage, and transmission projects (2026-2035)."""
    query = db.query(ProjectPipeline)
    if status:
        query = query.filter(ProjectPipeline.status == status)
    projects = query.order_by(ProjectPipeline.expected_cod_year.asc()).all()
    results = []
    for p in projects:
        results.append(ProjectPipelineResponse(
            id=p.id,
            name=p.name,
            technology=p.technology,
            capacity_mw=p.capacity_mw,
            storage_mwh=p.storage_mwh,
            latitude=p.latitude,
            longitude=p.longitude,
            bus_id=p.bus_id,
            status=p.status,
            expected_cod_year=p.expected_cod_year,
            owner=p.owner,
            estimated_capex_musd=p.estimated_capex_musd,
            description=p.description,
            bus_name=p.bus.name if p.bus else None
        ))
    return results

@router.get("/node-prices/{bus_id}", response_model=List[NodePriceResponse])
def get_node_prices(bus_id: int, limit: int = 72, db: Session = Depends(get_db)):
    """Retrieve historical time series of nodal marginal costs for a specific bus."""
    prices = db.query(NodePrice).filter(
        NodePrice.bus_id == bus_id
    ).order_by(NodePrice.timestamp.desc()).limit(limit).all()
    return list(reversed(prices))

@router.get("/generation-mix", response_model=List[GenerationHourlyResponse])
def get_generation_mix(limit: int = 48, db: Session = Depends(get_db)):
    """Retrieve hourly generation mix (Solar, Wind, Hydro, Gas, Coal, BESS, Curtailment) for the SEN."""
    gens = db.query(GenerationHourly).order_by(GenerationHourly.timestamp.desc()).limit(limit).all()
    results = []
    for g in reversed(gens):
        ren_mw = g.solar_mw + g.wind_mw + g.hydro_mw + g.bess_discharge_mw
        total_mw = g.total_generation_mw if g.total_generation_mw > 0 else 1.0
        results.append(GenerationHourlyResponse(
            id=g.id,
            timestamp=g.timestamp,
            solar_mw=g.solar_mw,
            wind_mw=g.wind_mw,
            hydro_mw=g.hydro_mw,
            thermal_gas_mw=g.thermal_gas_mw,
            thermal_coal_mw=g.thermal_coal_mw,
            bess_discharge_mw=g.bess_discharge_mw,
            bess_charge_mw=g.bess_charge_mw,
            total_generation_mw=g.total_generation_mw,
            curtailment_mw=g.curtailment_mw,
            renewable_share_pct=round((ren_mw / total_mw) * 100.0, 1)
        ))
    return results

@router.get("/demand-hourly", response_model=List[DemandHourlyResponse])
def get_demand_hourly(limit: int = 48, db: Session = Depends(get_db)):
    """Retrieve hourly demand profile and mining/data-center consumption breakdown."""
    demands = db.query(DemandHourly).order_by(DemandHourly.timestamp.desc()).limit(limit).all()
    return list(reversed(demands))

@router.get("/fuels", response_model=List[FuelPriceResponse])
def get_fuel_prices(db: Session = Depends(get_db)):
    """Retrieve latest fuel prices (LNG Quintero, LNG Mejillones, Coal, Diesel, Brent)."""
    fuels = db.query(FuelPrice).order_by(FuelPrice.timestamp.desc()).limit(15).all()
    return fuels

@router.get("/hydro", response_model=List[HydroBasinResponse])
def get_hydro_basins(db: Session = Depends(get_db)):
    """Retrieve latest hydrological basin storage and inflow status."""
    basins = db.query(HydroBasin).order_by(HydroBasin.timestamp.desc()).limit(10).all()
    return basins

@router.get("/node-opportunity-ranking", response_model=List[NodeOpportunityScoreResponse])
def get_node_opportunity_ranking(db: Session = Depends(get_db)):
    """Retrieve all electrical buses ranked by their Node Opportunity Score v0.1."""
    scores = db.query(NodeOpportunityScore).order_by(NodeOpportunityScore.total_score.desc()).all()
    results = []
    for s in scores:
        results.append(NodeOpportunityScoreResponse(
            id=s.id,
            bus_id=s.bus_id,
            bus_code=s.bus.code if s.bus else "N/A",
            bus_name=s.bus.name if s.bus else "N/A",
            zone=s.bus.zone if s.bus else "N/A",
            timestamp=s.timestamp,
            total_score=s.total_score,
            expected_price_score=s.expected_price_score,
            capture_price_solar_score=s.capture_price_solar_score,
            capture_price_wind_score=s.capture_price_wind_score,
            bess_arbitrage_score=s.bess_arbitrage_score,
            congestion_risk_score=s.congestion_risk_score,
            curtailment_risk_score=s.curtailment_risk_score,
            future_competition_score=s.future_competition_score,
            demand_growth_score=s.demand_growth_score,
            grid_expansion_score=s.grid_expansion_score,
            recommendation_level=s.recommendation_level,
            methodology_version=s.methodology_version
        ))
    return results

@router.post("/project-analyzer", response_model=ProjectEvaluationResult)
def evaluate_project_siting(req: ProjectEvaluationRequest, db: Session = Depends(get_db)):
    """
    Financial and Technical Project Siting Optimizer.
    Evaluates a Generation + BESS project configuration and ranks the Top 10 SEN buses by NPV and IRR.
    """
    evaluator = ProjectEvaluator(db=db)
    return evaluator.evaluate_project(req)

@router.post("/export/excel")
def export_excel_model(req: ProjectEvaluationRequest, db: Session = Depends(get_db)):
    """
    Generates and downloads a complete multi-tab Microsoft Excel Financial Model (SpreadsheetML)
    with executive summary, Top 10 siting ranking, and 25-year cash flow projections.
    """
    from fastapi.responses import Response
    from packages.energy.report_generator import InvestmentReportGenerator

    evaluator = ProjectEvaluator(db=db)
    result = evaluator.evaluate_project(req)
    xml_content = InvestmentReportGenerator.generate_excel_spreadsheetml(result)

    return Response(
        content=xml_content.encode("utf-8"),
        media_type="application/vnd.ms-excel",
        headers={
            "Content-Disposition": 'attachment; filename="modelo_financiero_sen_2035.xls"'
        }
    )

@router.post("/export/memo-html")
def export_investment_memo_html(req: ProjectEvaluationRequest, db: Session = Depends(get_db)):
    """
    Generates an institutional, printable Executive Investment Memorandum & Diligence Report.
    """
    from fastapi.responses import HTMLResponse
    from packages.energy.report_generator import InvestmentReportGenerator

    evaluator = ProjectEvaluator(db=db)
    result = evaluator.evaluate_project(req)
    html_content = InvestmentReportGenerator.generate_investment_memo_html(result)

    return HTMLResponse(content=html_content)

# ---------------------------------------------------------
# GOOGLE GEMINI AI COPILOT & REGULATORY INTELLIGENCE
# ---------------------------------------------------------

@router.post("/ai/thesis")
def generate_ai_investment_thesis(req: ProjectEvaluationRequest, db: Session = Depends(get_db)):
    """
    Generates a high-level institutional AI investment thesis with Google Gemini
    for the project configuration and highest-ranked SEN bus.
    """
    from packages.ai.energy_copilot import EnergyAICopilot
    evaluator = ProjectEvaluator(db=db)
    result = evaluator.evaluate_project(req)
    top_bus = result.top_buses_ranking[0].model_dump() if result.top_buses_ranking else {}

    copilot = EnergyAICopilot()
    thesis_md = copilot.generate_siting_thesis(req.model_dump(), top_bus)
    return {
        "project": req.model_dump(),
        "top_bus": top_bus,
        "thesis_markdown": thesis_md
    }

@router.post("/ai/regulatory-advisor")
def consult_regulatory_advisor(payload: dict):
    """
    Consults the AI Regulatory & Legal Engineering Advisor (Ana IA 2.0)
    for questions regarding DFL 4, Ley 21.505 BESS, DS 88 PMGD, and CNE norms.
    """
    from packages.ai.energy_copilot import EnergyAICopilot
    query = payload.get("query", "")
    if not query:
        return {"response_markdown": "Por favor ingresa una consulta sobre la normativa eléctrica chilena."}
    
    copilot = EnergyAICopilot()
    response_md = copilot.answer_regulatory_query(query)
    return {
        "query": query,
        "response_markdown": response_md
    }

@router.post("/ai/dispatch-synthesis")
def synthesize_dispatch_ai(db: Session = Depends(get_db)):
    """
    Analyzes the latest SEN dispatch mix and duck curve dynamics with Google Gemini.
    """
    from packages.ai.energy_copilot import EnergyAICopilot
    latest_gen = db.query(GenerationHourly).order_by(GenerationHourly.timestamp.desc()).first()
    latest_demand = db.query(DemandHourly).order_by(DemandHourly.timestamp.desc()).first()

    mix_data = []
    if latest_gen:
        tot = latest_gen.total_generation_mw or 10000.0
        mix_data = [
            {"tech": "Solar PV", "gen_mw": latest_gen.solar_mw, "share_pct": round((latest_gen.solar_mw / tot) * 100, 1)},
            {"tech": "Eólica", "gen_mw": latest_gen.wind_mw, "share_pct": round((latest_gen.wind_mw / tot) * 100, 1)},
            {"tech": "Hidroeléctrica", "gen_mw": latest_gen.hydro_mw, "share_pct": round((latest_gen.hydro_mw / tot) * 100, 1)},
            {"tech": "Gas Natural", "gen_mw": latest_gen.thermal_gas_mw, "share_pct": round((latest_gen.thermal_gas_mw / tot) * 100, 1)},
            {"tech": "BESS Storage", "gen_mw": latest_gen.bess_discharge_mw, "share_pct": round((latest_gen.bess_discharge_mw / tot) * 100, 1)},
        ]
    demand_mw = latest_demand.total_demand_mw if latest_demand else 9800.0

    copilot = EnergyAICopilot()
    synthesis_md = copilot.explain_dispatch_and_grid(mix_data, demand_mw)
    return {
        "demand_mw": demand_mw,
        "mix": mix_data,
        "synthesis_markdown": synthesis_md
    }
