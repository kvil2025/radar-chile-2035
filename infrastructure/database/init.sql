-- ==============================================================================
-- RADAR CHILE 2035 — Initial Database DDL Schema (PostgreSQL / TimescaleDB)
-- ==============================================================================

-- Enable TimescaleDB extension if available
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- 1. SOURCES
CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    provider VARCHAR(100) NOT NULL,
    url VARCHAR(500),
    country VARCHAR(50) DEFAULT 'GLOBAL',
    frequency VARCHAR(50) DEFAULT 'DAILY',
    reliability_score DOUBLE PRECISION DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_sources_provider ON sources (provider);

-- 2. INDICATORS (The 30 Master Series)
CREATE TABLE IF NOT EXISTS indicators (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) DEFAULT 'DAILY',
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    direction INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_indicators_code ON indicators (code);
CREATE INDEX IF NOT EXISTS ix_indicators_category ON indicators (category);

-- 3. OBSERVATIONS (Time-Series Data Points)
CREATE TABLE IF NOT EXISTS observations (
    id BIGSERIAL PRIMARY KEY,
    indicator_id INTEGER NOT NULL REFERENCES indicators(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    original_value DOUBLE PRECISION,
    original_unit VARCHAR(50),
    quality_status VARCHAR(50) DEFAULT 'VALID',
    source_timestamp TIMESTAMP WITH TIME ZONE,
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    CONSTRAINT uq_indicator_timestamp UNIQUE (indicator_id, timestamp)
);
CREATE INDEX IF NOT EXISTS ix_obs_indicator_time ON observations (indicator_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS ix_obs_quality_status ON observations (quality_status);

-- Convert to TimescaleDB hypertable if extension is loaded
-- SELECT create_hypertable('observations', 'timestamp', if_not_exists => TRUE);

-- 4. DERIVED INDICATORS
CREATE TABLE IF NOT EXISTS derived_indicators (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    formula VARCHAR(500) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. SIGNALS
CREATE TABLE IF NOT EXISTS signals (
    id SERIAL PRIMARY KEY,
    indicator_id INTEGER NOT NULL REFERENCES indicators(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    signal_type VARCHAR(100) NOT NULL,
    signal_strength DOUBLE PRECISION DEFAULT 0.0,
    value DOUBLE PRECISION NOT NULL,
    baseline DOUBLE PRECISION,
    metadata JSONB
);
CREATE INDEX IF NOT EXISTS ix_signals_time ON signals (timestamp DESC);

-- 6. SCORES (The 5 Strategic Indices)
CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    score_type VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    value DOUBLE PRECISION NOT NULL,
    confidence DOUBLE PRECISION DEFAULT 1.0,
    methodology_version VARCHAR(50) DEFAULT 'v0.1' NOT NULL,
    metadata JSONB
);
CREATE INDEX IF NOT EXISTS ix_scores_type_time ON scores (score_type, timestamp DESC);

-- 7. REGIMES
CREATE TABLE IF NOT EXISTS regimes (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    regime_code VARCHAR(100) NOT NULL,
    confidence DOUBLE PRECISION DEFAULT 0.85,
    primary_driver VARCHAR(255),
    rationale TEXT NOT NULL,
    indicators_state JSONB
);
CREATE INDEX IF NOT EXISTS ix_regimes_time ON regimes (timestamp DESC);

-- 8. SCENARIOS (S1 to S4)
CREATE TABLE IF NOT EXISTS scenarios (
    id SERIAL PRIMARY KEY,
    scenario_code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    probability DOUBLE PRECISION NOT NULL,
    probability_type VARCHAR(50) DEFAULT 'MODEL_ESTIMATE' NOT NULL,
    drivers JSONB,
    supporting_indicators JSONB,
    contradicting_indicators JSONB,
    expected_chile_effect TEXT NOT NULL,
    risk_level VARCHAR(50) DEFAULT 'MODERATE',
    opportunity_level VARCHAR(50) DEFAULT 'MODERATE',
    methodology_version VARCHAR(50) DEFAULT 'v0.1',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. TRANSMISSION CHANNELS
CREATE TABLE IF NOT EXISTS transmission_channels (
    id SERIAL PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    global_indicator_code VARCHAR(100) NOT NULL,
    chile_indicator_code VARCHAR(100) NOT NULL,
    transmission_speed VARCHAR(50) DEFAULT 'MEDIUM_TERM_1Q',
    elasticity DOUBLE PRECISION DEFAULT 1.0,
    description TEXT NOT NULL,
    current_impact_score DOUBLE PRECISION DEFAULT 0.0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. ALERTS
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    severity VARCHAR(50) DEFAULT 'INFO',
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    indicator_id INTEGER REFERENCES indicators(id) ON DELETE SET NULL,
    trigger_value DOUBLE PRECISION,
    current_value DOUBLE PRECISION,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS ix_alerts_status ON alerts (status);
CREATE INDEX IF NOT EXISTS ix_alerts_severity ON alerts (severity);

-- 11. INGESTION RUNS (Observability)
CREATE TABLE IF NOT EXISTS ingestion_runs (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP WITH TIME ZONE,
    duration_seconds DOUBLE PRECISION DEFAULT 0.0,
    records_received INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    records_rejected INTEGER DEFAULT 0,
    errors JSONB,
    status VARCHAR(50) DEFAULT 'RUNNING'
);

-- 12. RESEARCH DOCUMENTS
CREATE TABLE IF NOT EXISTS research_documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    source VARCHAR(255) NOT NULL,
    url VARCHAR(1000),
    published_at TIMESTAMP WITH TIME ZONE,
    retrieved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    category VARCHAR(100) NOT NULL,
    summary TEXT NOT NULL,
    relevance DOUBLE PRECISION DEFAULT 1.0,
    metadata JSONB
);
