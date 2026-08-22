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
    errors: Optional[list[str]] = None
    status: str

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
