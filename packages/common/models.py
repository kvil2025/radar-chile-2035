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
