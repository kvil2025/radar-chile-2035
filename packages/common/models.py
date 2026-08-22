import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, 
    JSON, Enum as SQLEnum, UniqueConstraint, Index, Boolean
)
from sqlalchemy.orm import relationship
from packages.common.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    provider = Column(String(100), nullable=False, index=True)
    url = Column(String(500), nullable=True)
    country = Column(String(50), default="GLOBAL")
    frequency = Column(String(50), default="DAILY")
    reliability_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    indicators = relationship("Indicator", back_populates="source")


class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)
    unit = Column(String(50), nullable=False)
    frequency = Column(String(50), default="DAILY")
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    direction = Column(Integer, default=1)  # +1 positive/expansion, -1 stress/tightening
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    source = relationship("Source", back_populates="indicators")
    observations = relationship("Observation", back_populates="indicator", cascade="all, delete-orphan")
    signals = relationship("Signal", back_populates="indicator", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="indicator")


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False)
    original_value = Column(Float, nullable=True)
    original_unit = Column(String(50), nullable=True)
    quality_status = Column(String(50), default="VALID", index=True)  # VALID, SUSPECT, MISSING, STALE, OUTLIER, INVALID
    source_timestamp = Column(DateTime, nullable=True)
    ingested_at = Column(DateTime, default=datetime.datetime.utcnow)
    metadata_json = Column("metadata", JSON, nullable=True)

    indicator = relationship("Indicator", back_populates="observations")

    __table_args__ = (
        UniqueConstraint("indicator_id", "timestamp", name="uq_indicator_timestamp"),
        Index("ix_obs_indicator_time", "indicator_id", "timestamp"),
    )


class DerivedIndicator(Base):
    __tablename__ = "derived_indicators"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    formula = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    signal_type = Column(String(100), nullable=False, index=True)
    signal_strength = Column(Float, default=0.0)  # -1.0 to +1.0
    value = Column(Float, nullable=False)
    baseline = Column(Float, nullable=True)
    metadata_json = Column("metadata", JSON, nullable=True)

    indicator = relationship("Indicator", back_populates="signals")


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    score_type = Column(String(100), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    value = Column(Float, nullable=False)
    confidence = Column(Float, default=1.0)
    methodology_version = Column(String(50), default="v0.1", nullable=False)
    metadata_json = Column("metadata", JSON, nullable=True)  # Includes contributors, weights, values


class Regime(Base):
    __tablename__ = "regimes"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    regime_code = Column(String(100), nullable=False, index=True)  # NORMAL, EXPANSION, FISCAL_STRESS, etc.
    confidence = Column(Float, default=0.85)
    primary_driver = Column(String(255), nullable=True)
    rationale = Column(Text, nullable=False)
    indicators_state = Column(JSON, nullable=True)


class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    scenario_code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    probability = Column(Float, nullable=False)
    probability_type = Column(String(50), default="MODEL_ESTIMATE", nullable=False)
    drivers = Column(JSON, nullable=True)
    supporting_indicators = Column(JSON, nullable=True)
    contradicting_indicators = Column(JSON, nullable=True)
    expected_chile_effect = Column(Text, nullable=False)
    risk_level = Column(String(50), default="MODERATE")
    opportunity_level = Column(String(50), default="MODERATE")
    methodology_version = Column(String(50), default="v0.1")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class TransmissionChannel(Base):
    __tablename__ = "transmission_channels"

    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String(255), nullable=False, index=True)
    global_indicator_code = Column(String(100), nullable=False)
    chile_indicator_code = Column(String(100), nullable=False)
    transmission_speed = Column(String(50), default="MEDIUM_TERM_1Q")
    elasticity = Column(Float, default=1.0)
    description = Column(Text, nullable=False)
    current_impact_score = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    severity = Column(String(50), default="INFO", index=True)  # INFO, WATCH, WARNING, CRITICAL
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    indicator_id = Column(Integer, ForeignKey("indicators.id"), nullable=True)
    trigger_value = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    status = Column(String(50), default="ACTIVE", index=True)  # ACTIVE, ACKNOWLEDGED, RESOLVED
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)

    indicator = relationship("Indicator", back_populates="alerts")


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String(100), nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, default=0.0)
    records_received = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_rejected = Column(Integer, default=0)
    errors = Column(JSON, nullable=True)
    status = Column(String(50), default="RUNNING")


class ResearchDocument(Base):
    __tablename__ = "research_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    source = Column(String(255), nullable=False)
    url = Column(String(1000), nullable=True)
    published_at = Column(DateTime, nullable=True)
    retrieved_at = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String(100), nullable=False)
    summary = Column(Text, nullable=False)
    relevance = Column(Float, default=1.0)
    metadata_json = Column("metadata", JSON, nullable=True)


# ==============================================================================
# ENERGY & SEN GRID MODELS (CHILE 2035)
# ==============================================================================

class Substation(Base):
    __tablename__ = "substations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    voltage_levels = Column(String(100), default="220/500 kV")
    capacity_mva = Column(Float, nullable=True)
    operator = Column(String(255), default="Transelec")
    status = Column(String(50), default="OPERATIONAL")

    buses = relationship("Bus", back_populates="substation")


class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    voltage_kv = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    zone = Column(String(50), nullable=False, index=True)  # NORTE_GRANDE, NORTE_CHICO, CENTRO, SUR
    region = Column(String(100), nullable=False)
    substation_id = Column(Integer, ForeignKey("substations.id"), nullable=True)
    status = Column(String(50), default="OPERATIONAL")

    substation = relationship("Substation", back_populates="buses")
    generation_plants = relationship("GenerationPlant", back_populates="bus")
    bess_units = relationship("BessUnit", back_populates="bus")
    projects = relationship("ProjectPipeline", back_populates="bus")
    node_prices = relationship("NodePrice", back_populates="bus", cascade="all, delete-orphan")
    opportunity_scores = relationship("NodeOpportunityScore", back_populates="bus", cascade="all, delete-orphan")


class TransmissionLine(Base):
    __tablename__ = "transmission_lines"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    from_bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    to_bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    voltage_kv = Column(Float, nullable=False)
    capacity_mw = Column(Float, nullable=False)
    length_km = Column(Float, nullable=False)
    impedance_ohm = Column(Float, default=0.05)
    status = Column(String(50), default="OPERATIONAL")
    commission_date = Column(DateTime, nullable=True)

    from_bus = relationship("Bus", foreign_keys=[from_bus_id])
    to_bus = relationship("Bus", foreign_keys=[to_bus_id])
    congestion_events = relationship("CongestionEvent", back_populates="line")


class GenerationPlant(Base):
    __tablename__ = "generation_plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    technology = Column(String(100), nullable=False, index=True)  # SOLAR_PV, WIND, HYDRO_RESERVOIR, HYDRO_ROR, THERMAL_GAS, THERMAL_COAL, BESS, BIOMASS
    capacity_mw = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    operator = Column(String(255), default="Desconocido")
    status = Column(String(50), default="OPERATIONAL")
    capacity_factor_avg = Column(Float, default=0.30)
    commission_date = Column(DateTime, nullable=True)

    bus = relationship("Bus", back_populates="generation_plants")


class BessUnit(Base):
    __tablename__ = "bess_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    power_mw = Column(Float, nullable=False)
    energy_mwh = Column(Float, nullable=False)
    duration_hours = Column(Float, default=4.0)
    round_trip_efficiency = Column(Float, default=0.85)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    operator = Column(String(255), default="Operador")
    status = Column(String(50), default="OPERATIONAL")
    commission_date = Column(DateTime, nullable=True)

    bus = relationship("Bus", back_populates="bess_units")


class ProjectPipeline(Base):
    __tablename__ = "projects_pipeline"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    technology = Column(String(100), nullable=False, index=True)  # SOLAR_PV, WIND, BESS, SOLAR_PLUS_BESS, TRANSMISSION
    capacity_mw = Column(Float, default=0.0)
    storage_mwh = Column(Float, default=0.0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=True)
    status = Column(String(50), default="DEVELOPMENT", index=True)  # ANNOUNCED, PERMITTED_RCA, DEVELOPMENT, FINANCING, CONSTRUCTION, OPERATIONAL
    expected_cod_year = Column(Integer, default=2028, index=True)
    owner = Column(String(255), default="Desarrollador")
    estimated_capex_musd = Column(Float, default=100.0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    bus = relationship("Bus", back_populates="projects")


class NodePrice(Base):
    __tablename__ = "node_prices"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    price_usd_mwh = Column(Float, nullable=False)
    marginal_energy_cost = Column(Float, default=0.0)
    marginal_loss_cost = Column(Float, default=0.0)
    marginal_congestion_cost = Column(Float, default=0.0)
    quality_status = Column(String(50), default="VALID")

    bus = relationship("Bus", back_populates="node_prices")

    __table_args__ = (
        UniqueConstraint("bus_id", "timestamp", name="uq_bus_timestamp"),
        Index("ix_node_prices_bus_time", "bus_id", "timestamp"),
    )


class CongestionEvent(Base):
    __tablename__ = "congestion_events"

    id = Column(Integer, primary_key=True, index=True)
    line_id = Column(Integer, ForeignKey("transmission_lines.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    flow_mw = Column(Float, nullable=False)
    capacity_mw = Column(Float, nullable=False)
    utilization_pct = Column(Float, nullable=False)
    is_congested = Column(Boolean, default=False)

    line = relationship("TransmissionLine", back_populates="congestion_events")


class GenerationHourly(Base):
    __tablename__ = "generation_hourly"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, unique=True, index=True)
    solar_mw = Column(Float, default=0.0)
    wind_mw = Column(Float, default=0.0)
    hydro_mw = Column(Float, default=0.0)
    thermal_gas_mw = Column(Float, default=0.0)
    thermal_coal_mw = Column(Float, default=0.0)
    bess_discharge_mw = Column(Float, default=0.0)
    bess_charge_mw = Column(Float, default=0.0)
    total_generation_mw = Column(Float, default=0.0)
    curtailment_mw = Column(Float, default=0.0)


class DemandHourly(Base):
    __tablename__ = "demand_hourly"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    zone = Column(String(50), nullable=False, index=True)  # SEN_TOTAL, NORTE_GRANDE, NORTE_CHICO, CENTRO, SUR
    total_demand_mw = Column(Float, nullable=False)
    mining_demand_mw = Column(Float, default=0.0)
    industrial_demand_mw = Column(Float, default=0.0)
    residential_demand_mw = Column(Float, default=0.0)
    data_centers_demand_mw = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint("zone", "timestamp", name="uq_zone_demand_timestamp"),
    )


class FuelPrice(Base):
    __tablename__ = "fuel_prices"

    id = Column(Integer, primary_key=True, index=True)
    fuel_type = Column(String(100), nullable=False, index=True)  # LNG_QUINTERO, LNG_MEJILLONES, COAL_API2, DIESEL, BRENT
    timestamp = Column(DateTime, nullable=False, index=True)
    price_usd = Column(Float, nullable=False)
    unit = Column(String(50), default="USD/MMBtu")


class HydroBasin(Base):
    __tablename__ = "hydro_basins"

    id = Column(Integer, primary_key=True, index=True)
    basin_name = Column(String(100), nullable=False)  # MAULE, LAJA, BIOBIO, RAPEL
    reservoir_name = Column(String(100), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    inflow_m3s = Column(Float, default=0.0)
    storage_m3_million = Column(Float, default=0.0)
    usable_percentage = Column(Float, default=50.0)
    hydro_year_type = Column(String(50), default="NORMAL")  # DRY, NORMAL, WET


class NodeOpportunityScore(Base):
    __tablename__ = "node_opportunity_scores"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    total_score = Column(Float, nullable=False)  # 0 to 100
    expected_price_score = Column(Float, default=50.0)
    capture_price_solar_score = Column(Float, default=50.0)
    capture_price_wind_score = Column(Float, default=50.0)
    bess_arbitrage_score = Column(Float, default=50.0)
    congestion_risk_score = Column(Float, default=50.0)
    curtailment_risk_score = Column(Float, default=50.0)
    future_competition_score = Column(Float, default=50.0)
    demand_growth_score = Column(Float, default=50.0)
    grid_expansion_score = Column(Float, default=50.0)
    recommendation_level = Column(String(50), default="MODERATE")  # HIGHLY_ATTRACTIVE, ATTRACTIVE, MODERATE, RISKY, AVOID
    methodology_version = Column(String(50), default="v0.1")
    metadata_json = Column("metadata", JSON, nullable=True)

    bus = relationship("Bus", back_populates="opportunity_scores")
