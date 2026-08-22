import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field

# Base schema with ORM mode enabled
class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# ----------------- SOURCES -----------------
class SourceBase(SchemaBase):
    name: str
    provider: str
    url: Optional[str] = None
    country: str = "GLOBAL"
    frequency: str = "DAILY"
    reliability_score: float = 1.0

class SourceCreate(SourceBase):
    pass

class SourceResponse(SourceBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

# ----------------- INDICATORS -----------------
class IndicatorBase(SchemaBase):
    code: str
    name: str
    description: Optional[str] = None
    category: str
    unit: str
    frequency: str = "DAILY"
    direction: int = 1
    source_id: Optional[int] = None

class IndicatorCreate(IndicatorBase):
    pass

class IndicatorResponse(IndicatorBase):
    id: int
    created_at: datetime.datetime

# ----------------- OBSERVATIONS -----------------
class ObservationBase(SchemaBase):
    indicator_id: int
    timestamp: datetime.datetime
    value: float
    original_value: Optional[float] = None
    original_unit: Optional[str] = None
    quality_status: str = "VALID"
    source_timestamp: Optional[datetime.datetime] = None
    metadata_json: Optional[dict[str, Any]] = None

class ObservationCreate(ObservationBase):
    pass

class ObservationResponse(ObservationBase):
    id: int
    ingested_at: datetime.datetime

class IndicatorWithObservations(IndicatorResponse):
    observations: list[ObservationResponse] = []
    latest_value: Optional[float] = None
    latest_timestamp: Optional[datetime.datetime] = None
    change_yoy: Optional[float] = None
    change_mom: Optional[float] = None
    z_score: Optional[float] = None

# ----------------- SCORES -----------------
class ScoreContributor(BaseModel):
    indicator_code: str
    indicator_name: str
    weight: float
    raw_value: float
    normalized_value: float
    contribution_points: float
    direction: int
    unit: str

class ScoreResponse(SchemaBase):
    id: int
    score_type: str
    timestamp: datetime.datetime
    value: float
    confidence: float
    methodology_version: str = "v0.1"
    metadata_json: Optional[dict[str, Any]] = None
    contributors: list[ScoreContributor] = []
    trend: str = "STABLE"  # UP, DOWN, STABLE
    delta_30d: float = 0.0

# ----------------- REGIMES -----------------
class RegimeResponse(SchemaBase):
    id: int
    timestamp: datetime.datetime
    regime_code: str
    confidence: float
    primary_driver: Optional[str] = None
    rationale: str
    indicators_state: Optional[dict[str, Any]] = None

# ----------------- SCENARIOS -----------------
class ScenarioResponse(SchemaBase):
    id: int
    scenario_code: str
    name: str
    description: str
    probability: float
    probability_type: str = "MODEL_ESTIMATE"
    drivers: Optional[list[str]] = None
    supporting_indicators: Optional[list[str]] = None
    contradicting_indicators: Optional[list[str]] = None
    expected_chile_effect: str
    risk_level: str
    opportunity_level: str
    methodology_version: str = "v0.1"
    updated_at: datetime.datetime

# ----------------- TRANSMISSION & CHILE IMPACT -----------------
class TransmissionChannelResponse(SchemaBase):
    id: int
    channel_name: str
    global_indicator_code: str
    chile_indicator_code: str
    transmission_speed: str
    elasticity: float
    description: str
    current_impact_score: float
    updated_at: datetime.datetime

class ChileImpactOverview(BaseModel):
    net_opportunity_score: float
    primary_positive_channel: str
    primary_risk_channel: str
    channels: list[TransmissionChannelResponse]

# ----------------- ALERTS -----------------
class AlertResponse(SchemaBase):
    id: int
    severity: str
    title: str
    description: str
    indicator_id: Optional[int] = None
    indicator_code: Optional[str] = None
    trigger_value: Optional[float] = None
    current_value: Optional[float] = None
    status: str
    created_at: datetime.datetime
    resolved_at: Optional[datetime.datetime] = None

# ----------------- INGESTION RUNS -----------------
class IngestionRunResponse(SchemaBase):
    id: int
    source_name: str
    started_at: datetime.datetime
    finished_at: Optional[datetime.datetime] = None
    duration_seconds: float
    records_received: int
    records_inserted: int
    records_rejected: int
    status: str
    errors: Optional[list[str]] = None

# ----------------- RESEARCH DOCUMENTS -----------------
class ResearchDocumentResponse(SchemaBase):
    id: int
    title: str
    source: str
    url: Optional[str] = None
    published_at: Optional[datetime.datetime] = None
    category: str
    summary: str
    relevance: float


# ==============================================================================
# ENERGY SCHEMAS (SEN CHILE 2035)
# ==============================================================================

class SubstationResponse(SchemaBase):
    id: int
    code: str
    name: str
    latitude: float
    longitude: float
    voltage_levels: str
    capacity_mva: Optional[float] = None
    operator: str
    status: str

class BusBase(SchemaBase):
    code: str
    name: str
    voltage_kv: float
    latitude: float
    longitude: float
    zone: str
    region: str
    substation_id: Optional[int] = None
    status: str = "OPERATIONAL"

class BusResponse(BusBase):
    id: int
    latest_price: Optional[float] = None
    opportunity_score: Optional[float] = None
    recommendation_level: Optional[str] = None

class TransmissionLineResponse(SchemaBase):
    id: int
    code: str
    name: str
    from_bus_id: int
    to_bus_id: int
    voltage_kv: float
    capacity_mw: float
    length_km: float
    impedance_ohm: float
    status: str
    from_bus_name: Optional[str] = None
    to_bus_name: Optional[str] = None
    current_flow_mw: Optional[float] = None
    utilization_pct: Optional[float] = None
    is_congested: bool = False

class GenerationPlantResponse(SchemaBase):
    id: int
    name: str
    technology: str
    capacity_mw: float
    latitude: float
    longitude: float
    bus_id: int
    operator: str
    status: str
    capacity_factor_avg: float
    bus_name: Optional[str] = None

class BessUnitResponse(SchemaBase):
    id: int
    name: str
    power_mw: float
    energy_mwh: float
    duration_hours: float
    round_trip_efficiency: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bus_id: int
    operator: str
    status: str
    bus_name: Optional[str] = None

class ProjectPipelineResponse(SchemaBase):
    id: int
    name: str
    technology: str
    capacity_mw: float
    storage_mwh: float
    latitude: float
    longitude: float
    bus_id: Optional[int] = None
    status: str
    expected_cod_year: int
    owner: str
    estimated_capex_musd: float
    description: Optional[str] = None
    bus_name: Optional[str] = None

class NodePriceResponse(SchemaBase):
    id: int
    bus_id: int
    timestamp: datetime.datetime
    price_usd_mwh: float
    marginal_energy_cost: float
    marginal_loss_cost: float
    marginal_congestion_cost: float
    quality_status: str

class GenerationHourlyResponse(SchemaBase):
    id: int
    timestamp: datetime.datetime
    solar_mw: float
    wind_mw: float
    hydro_mw: float
    thermal_gas_mw: float
    thermal_coal_mw: float
    bess_discharge_mw: float
    bess_charge_mw: float
    total_generation_mw: float
    curtailment_mw: float
    renewable_share_pct: Optional[float] = None

class DemandHourlyResponse(SchemaBase):
    id: int
    timestamp: datetime.datetime
    zone: str
    total_demand_mw: float
    mining_demand_mw: float
    industrial_demand_mw: float
    residential_demand_mw: float
    data_centers_demand_mw: float

class FuelPriceResponse(SchemaBase):
    id: int
    fuel_type: str
    timestamp: datetime.datetime
    price_usd: float
    unit: str

class HydroBasinResponse(SchemaBase):
    id: int
    basin_name: str
    reservoir_name: str
    timestamp: datetime.datetime
    inflow_m3s: float
    storage_m3_million: float
    usable_percentage: float
    hydro_year_type: str

class NodeOpportunityScoreResponse(SchemaBase):
    id: int
    bus_id: int
    bus_code: Optional[str] = None
    bus_name: Optional[str] = None
    zone: Optional[str] = None
    timestamp: datetime.datetime
    total_score: float
    expected_price_score: float
    capture_price_solar_score: float
    capture_price_wind_score: float
    bess_arbitrage_score: float
    congestion_risk_score: float
    curtailment_risk_score: float
    future_competition_score: float
    demand_growth_score: float
    grid_expansion_score: float
    recommendation_level: str
    methodology_version: str

class BusRankingItem(BaseModel):
    rank: int
    bus_id: int
    bus_code: str
    bus_name: str
    zone: str
    region: str
    opportunity_score: float
    recommendation_level: str
    avg_price_usd_mwh: float
    capture_price_solar: float
    capture_price_wind: float
    bess_arbitrage_spread: float
    curtailment_risk: str
    congestion_risk: str
    npv_musd: float
    irr_pct: float
    lcoe_usd_mwh: float
    payback_years: float
    summary_rationale: str

class ProjectEvaluationRequest(BaseModel):
    technology: str = Field(default="SOLAR_PLUS_BESS", description="SOLAR_PV, WIND, BESS, SOLAR_PLUS_BESS")
    capacity_mw: float = Field(default=100.0, description="Potencia nominal en MW")
    storage_mwh: float = Field(default=400.0, description="Capacidad de almacenamiento BESS en MWh (4h)")
    target_cod_year: int = Field(default=2029, description="Año estimado de entrada en operación comercial (COD)")
    lifetime_years: int = Field(default=25, description="Vida útil del proyecto en años")
    custom_capex_musd: Optional[float] = Field(None, description="CAPEX estimado en millones de USD (opcional)")
    custom_opex_musd_year: Optional[float] = Field(None, description="OPEX anual en millones de USD (opcional)")
    discount_rate_pct: float = Field(default=8.0, description="Tasa de descuento para NPV en %")

class ProjectEvaluationResult(BaseModel):
    request: ProjectEvaluationRequest
    estimated_capex_musd: float
    estimated_opex_musd_year: float
    top_buses_ranking: list[BusRankingItem]
    methodology: str
    timestamp: datetime.datetime
