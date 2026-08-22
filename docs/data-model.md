# RADAR CHILE 2035 — Modelo de Datos (Data Model)

## 1. Tablas Principales

### `sources`
Registro de instituciones y proveedores oficiales de datos.
- `id` (UUID / Integer, PK)
- `name` (String, e.g. "Federal Reserve Bank of St. Louis")
- `provider` (String, e.g. "FRED", "BANCO_CENTRAL_CHILE", "YAHOO_FINANCE", "WORLD_BANK", "COCHILCO")
- `url` (String)
- `country` (String, e.g. "USA", "CHL", "GLOBAL", "CHN")
- `frequency` (String, e.g. "DAILY", "MONTHLY", "QUARTERLY")
- `reliability_score` (Float, 0.0 - 1.0)
- `created_at`, `updated_at` (DateTime UTC)

### `indicators`
Catálogo maestro de las 30 variables fundamentales y series de tiempo.
- `id` (UUID / Integer, PK)
- `code` (String UNIQUE, e.g. "US10Y", "COPPER", "CLP_USD")
- `name` (String, e.g. "US 10-Year Treasury Constant Maturity Rate")
- `description` (Text)
- `category` (String, e.g. "MACRO_USA", "MONETARY", "COMMODITIES", "CHINA", "CHILE", "MINING", "ENERGY_TECH")
- `unit` (String, e.g. "%", "USD/lb", "USD/oz", "CLP/USD", "Index")
- `frequency` (String, e.g. "DAILY", "MONTHLY")
- `source_id` (FK -> `sources.id`)
- `direction` (Integer, +1 = mayor valor es expansivo/positivo, -1 = mayor valor representa estrés/presión)
- `created_at` (DateTime UTC)

### `observations`
Puntos de serie temporal observados de forma empírica.
- `id` (UUID / BigInteger, PK)
- `indicator_id` (FK -> `indicators.id`, INDEX)
- `timestamp` (DateTime UTC, INDEX)
- `value` (Float, NOT NULL)
- `original_value` (Float)
- `original_unit` (String)
- `quality_status` (Enum: `VALID`, `SUSPECT`, `MISSING`, `STALE`, `OUTLIER`, `INVALID`)
- `source_timestamp` (DateTime UTC)
- `ingested_at` (DateTime UTC)
- `metadata` (JSONB)
- *Constraint*: UNIQUE(`indicator_id`, `timestamp`)

### `derived_indicators`
Definición de fórmulas y series transformadas.
- `id` (UUID / Integer, PK)
- `code` (String UNIQUE, e.g. "YIELD_SPREAD_10Y_2Y", "COPPER_GOLD_RATIO", "REAL_RATE_US")
- `name` (String)
- `formula` (String, e.g. "US10Y - US2Y", "COPPER / GOLD")
- `description` (Text)
- `category` (String)
- `created_at` (DateTime UTC)

### `signals`
Detección cuantitativa de quiebres técnicos o anomalías.
- `id` (UUID / Integer, PK)
- `indicator_id` (FK -> `indicators.id`)
- `timestamp` (DateTime UTC)
- `signal_type` (String, e.g. "YIELD_CURVE_INVERSION", "BREAKOUT_200MA", "Z_SCORE_ANOMALY")
- `signal_strength` (Float, -1.0 a +1.0)
- `value` (Float)
- `baseline` (Float)
- `metadata` (JSONB)

### `scores`
Valores calculados de los 5 índices estratégicos.
- `id` (UUID / Integer, PK)
- `score_type` (String, e.g. "DOLLAR_STRESS", "MONETARY_STRESS", "COMMODITY_CYCLE", "MINING_CYCLE", "CHILE_OPPORTUNITY")
- `timestamp` (DateTime UTC)
- `value` (Float, 0.0 - 100.0)
- `confidence` (Float, 0.0 - 1.0)
- `methodology_version` (String, e.g. "v0.1")
- `metadata` (JSONB con desglose completo de `contributors`, pesos y valores)

### `regimes`
Clasificación de régimen macroeconómico global.
- `id` (UUID / Integer, PK)
- `timestamp` (DateTime UTC)
- `regime_code` (Enum: `NORMAL`, `EXPANSION`, `TRANSITION`, `FISCAL_STRESS`, `INFLATIONARY`, `RECESSION`, `COMMODITY_SUPERCYCLE`, `MONETARY_STRESS`)
- `confidence` (Float, 0.0 - 1.0)
- `primary_driver` (String)
- `rationale` (Text)
- `indicators_state` (JSONB)

### `scenarios`
Evaluación cuantitativa de los 4 escenarios macroeconómicos.
- `id` (UUID / Integer, PK)
- `scenario_code` (String, e.g. "S1_SOFT_LANDING", "S2_FISCAL_DOMINANCE", "S3_GLOBAL_RECESSION", "S4_COMMODITY_SUPERCYCLE")
- `name` (String)
- `description` (Text)
- `probability` (Float, 0.0 - 1.0)
- `probability_type` (String, "MODEL_ESTIMATE")
- `supporting_indicators` (JSONB)
- `contradicting_indicators` (JSONB)
- `expected_chile_effect` (Text)
- `risk_level` (String, "LOW", "MODERATE", "HIGH", "CRITICAL")
- `opportunity_level` (String, "LOW", "MODERATE", "HIGH", "TRANSFORMATIVE")
- `updated_at` (DateTime UTC)

### `transmission_channels`
Matriz de relaciones causa-efecto global → Chile.
- `id` (UUID / Integer, PK)
- `channel_name` (String, e.g. "US_RATES_TO_CLP", "COPPER_TO_FISCAL_REVENUE")
- `global_indicator_id` (FK -> `indicators.id`)
- `chile_indicator_id` (FK -> `indicators.id`)
- `transmission_speed` (String, "IMMEDIATE_1D", "SHORT_TERM_1M", "MEDIUM_TERM_1Q", "STRUCTURAL_1Y")
- `elasticity` (Float)
- `description` (Text)
- `current_impact_score` (Float, -100.0 a +100.0)

### `alerts`
Alertas del sistema con umbrales y seguimiento.
- `id` (UUID / Integer, PK)
- `severity` (Enum: `INFO`, `WATCH`, `WARNING`, `CRITICAL`)
- `title` (String)
- `description` (Text)
- `indicator_id` (FK -> `indicators.id`, Nullable)
- `trigger_value` (Float)
- `current_value` (Float)
- `status` (Enum: `ACTIVE`, `ACKNOWLEDGED`, `RESOLVED`)
- `created_at` (DateTime UTC)
- `resolved_at` (DateTime UTC, Nullable)

### `ingestion_runs`
Trazabilidad y observabilidad del pipeline de datos.
- `id` (UUID / Integer, PK)
- `source_name` (String)
- `started_at` (DateTime UTC)
- `finished_at` (DateTime UTC)
- `duration_seconds` (Float)
- `records_received` (Integer)
- `records_inserted` (Integer)
- `records_rejected` (Integer)
- `errors` (JSONB)
- `status` (String: "SUCCESS", "PARTIAL", "FAILED")

### `research_documents`
Repositorio de documentos y reportes para futura capa RAG.
- `id` (UUID / Integer, PK)
- `title` (String)
- `source` (String)
- `url` (String)
- `published_at` (DateTime UTC)
- `retrieved_at` (DateTime UTC)
- `category` (String)
- `summary` (Text)
- `relevance` (Float)
- `metadata` (JSONB)
