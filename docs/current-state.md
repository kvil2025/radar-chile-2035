# RADAR CHILE 2035 — Diagnóstico del Estado Actual (Current State)

**Fecha**: 2026-08-21  
**Autor**: Senior Staff Software Engineer & Quantitative Architect  
**Fase**: FASE 0 — Arquitectura y Diagnóstico  

---

## 1. Inspección del Repositorio Actual

### Estado Físico
- **Directorio de trabajo**: `/Users/cavila/.gemini/antigravity/scratch/radar_chile`
- **Estado**: Workspace limpio / Lienzo en blanco (Greenfield).
- **Herramientas de entorno disponibles en el host**:
  - Python: `3.12.8` (`/usr/local/bin/python3.12`) y `3.9.12`
  - Node.js: `v22.17.0`
  - Git: `2.51.0`
  - Bóveda de credenciales (`~/.secrets/tokens.env`) disponible con API keys y configuraciones base.

### Conclusión de Diagnóstico
Al tratarse de un inicio greenfield, no existen deudas técnicas heredadas, código deprecado ni conflictos de dependencias. Se tiene la oportunidad óptima para estructurar la arquitectura del monorepo siguiendo las mejores prácticas de **Clean Architecture**, **Domain-Driven Design (DDD)** para finanzas cuantitativas, y separación estricta entre la capa de ingestión, validación, cálculo de indicadores, scoring, regímenes, escenarios y visualización.

---

## 2. Mapa de Componentes Objetivo

```text
radar-chile-2035/
│
├── apps/
│   ├── api/                     # Backend FastAPI (REST API, OpenAPI, Pydantic v2)
│   │   ├── src/
│   │   │   ├── routers/         # Endpoints modulares (/sources, /indicators, /scores, /regimes, etc.)
│   │   │   ├── dependencies.py  # Inyección de dependencias (DB, Auth, Services)
│   │   │   └── main.py          # Entrypoint FastAPI con middlewares de seguridad y CORS
│   │   └── Dockerfile
│   │
│   └── web/                     # Frontend Next.js 15 / React 19 / TypeScript / Tailwind / Recharts
│       ├── src/
│       │   ├── components/      # UI components (RadarHeader, ScoreCard, ExplainabilityModal, etc.)
│       │   ├── lib/             # API clients, formatters, maths
│       │   ├── app/             # App router pages (Dashboard, Scenarios, Indicators, Alerts)
│       │   └── styles/          # Design system Ávila Elgueta (Glassmorphism, Dark #0A0A0B, Navy/Gold/Cyan)
│       └── Dockerfile
│
├── packages/
│   ├── common/                  # Modelos Pydantic compartidos, Database ORM (SQLAlchemy 2.0), Config
│   │   ├── database.py          # Async/Sync engine, connection pool, session maker
│   │   ├── models.py            # Tablas SQLAlchemy: sources, indicators, observations, scores, etc.
│   │   ├── schemas.py           # Esquemas Pydantic v2 para validación bidireccional
│   │   └── config.py            # Settings tipados con pydantic-settings
│   │
│   ├── data/                    # Conectores de datos y Data Quality Engine
│   │   ├── connectors/          # BaseConnector, FRED, BancoCentral, Commodities, WorldBank, INE
│   │   ├── quality/             # Observation Quality Validator (VALID, SUSPECT, OUTLIER, etc.)
│   │   └── pipeline.py          # Ingestion runner idempotente con registro de runs
│   │
│   ├── indicators/              # Motor de Indicadores Derivados
│   │   ├── transformations.py   # YoY, MoM, Rolling Mean, Volatility, Z-Scores, Drawdown
│   │   └── derived_engine.py    # Yield Spreads, Real Rates, Gold/Copper ratio, Dollar Stress comps
│   │
│   ├── scoring/                 # Motor Cuantitativo de Scoring (Versionado v0.1)
│   │   ├── normalizers.py       # MinMax, Robust Z-score, Sigmoid transformations
│   │   ├── engine.py            # Dollar Stress, Monetary Stress, Commodity, Mining, Chile Opportunity
│   │   └── explainability.py    # Desglose transparente de contribuciones (WHY?)
│   │
│   ├── scenarios/               # Motor de Regímenes, Escenarios y Transmisión Chile
│   │   ├── regimes.py           # Clasificador de 8 regímenes económicos basados en evidencia
│   │   ├── scenario_engine.py   # Modelado de S1 Soft Landing, S2 Fiscal Dom, S3 Recession, S4 Supercycle
│   │   ├── chile_impact.py      # Canales de transmisión macro global → economía chilena
│   │   └── alerts.py            # Motor de alertas con umbrales y severidades (INFO, WATCH, WARNING, CRITICAL)
│   │
├── workers/                     # Tareas periódicas y pipelines de reconciliación
│   ├── ingestion_worker.py      # Ingesta periódica de fuentes
│   ├── recalculation_worker.py  # Recálculo de indicadores, scores y regímenes
│   └── alert_evaluator.py       # Evaluación continua de condiciones de alerta
│
├── infrastructure/
│   ├── docker/                  # Dockerfiles y scripts de build
│   └── database/
│       ├── migrations/          # Scripts Alembic para evolución de esquema
│       └── init.sql             # Script DDL inicial para PostgreSQL / TimescaleDB
│
├── tests/
│   ├── unit/                    # Tests unitarios (conectores, normalización, scoring, regímenes)
│   ├── integration/             # Tests de endpoints FastAPI y flujos DB
│   └── data_quality/            # Tests de integridad temporal, gaps, duplicados y outliers
│
├── docs/                        # Documentación técnica y metodológica completa
├── scripts/                     # Scripts de utilidad (seed_data.py, run_pipeline.py)
├── .env.example
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 3. Riesgos Técnicos y Mitigaciones

| Riesgo Técnico | Impacto | Estrategia de Mitigación |
|----------------|---------|--------------------------|
| **Rate limits o indisponibilidad en APIs públicas (FRED, Banco Central, etc.)** | Alto | Implementar sistema de retries con exponential backoff, caching de observaciones, idempotencia por timestamp y fallbacks de datos de contingencia con trazabilidad. |
| **Gaps temporales o frecuencias heterogéneas (diario, mensual, trimestral)** | Alto | Normalización explícita de series temporales con metadatos de frecuencia. No interpolar arbitrariamente sin documentar el método. Respetar `quality_status = STALE` cuando el dato no se ha actualizado. |
| **Pérdida de trazabilidad en fórmulas de scores** | Crítico | Cada score computado almacena su `methodology_version` (ej. `v0.1`), desglose de pesos de componentes (`contributors`), baseline y timestamp exacto. |
| **Confusión entre datos observados y proyecciones** | Crítico | Separación estricta a nivel de esquema: `observations` (hechos verificados con fuente y URL), `scores` (indicadores ponderados), `scenarios` (estimaciones de modelo etiquetadas obligatoriamente como `MODEL_ESTIMATE`). |
| **Bloqueo por dependencias externas en tests** | Medio | Arquitectura desacoplada mediante Repository Pattern y Dependency Injection. Pruebas unitarias con mocks deterministas y fixtures históricos. |

---

## 4. Primeras 5 Fuentes de Datos Oficiales Recomendadas

1. **FRED (Federal Reserve Economic Data - St. Louis Fed)**:
   - *Variables*: US10Y (DGS10), US30Y (DGS30), US2Y (DGS2), US_CPI (CPIAUCSL), US_FED_RATE (FEDFUNDS), US_FISCAL_DEFICIT (FYFSD), US_DEBT (GFDEBTN), DXY (DTWEXBGS / DTWEXAFEGS).
   - *Confiabilidad*: 99.9% (API REST oficial, documentada, con frecuencia diaria y mensual).

2. **Banco Central de Chile (Base de Datos Estadísticos - SIEL/API & Series Oficiales)**:
   - *Variables*: CLP_USD (Tipo de cambio observado), CHILE_TPM (Tasa de Política Monetaria), CHILE_CPI (IPC variación mensual/anual), CHILE_IMACEC (Índice Mensual de Actividad Económica), CHILE_GDP (PIB trimestral).
   - *Confiabilidad*: 99.5% (Fuente primaria oficial del Estado de Chile).

3. **Global Commodities & Financial Markets Connector (Yahoo Finance / Stooq / Metals)**:
   - *Variables*: COPPER (HG=F / Copper Futures LME/COMEX), GOLD (GC=F), OIL Brent (BZ=F), IRON ORE (TIO=F), LITHIUM proxy index.
   - *Confiabilidad*: 99.0% (Cotizaciones diarias de mercados internacionales).

4. **World Bank & OECD Open Data APIs**:
   - *Variables*: CHINA_PMI, CHINA_INDUSTRIAL_PRODUCTION, USD_RESERVES_SHARE (IMF COFER data), Foreign Treasury Holdings.
   - *Confiabilidad*: 99.0% (APIs REST abiertas en formato JSON/SDMX sin requerir autenticación restrictiva).

5. **Cochilco & INE Chile (Comisión Chilena del Cobre / Instituto Nacional de Estadísticas)**:
   - *Variables*: CHILE_COPPER_PRODUCTION (Producción mensual de cobre mina), CHILE_MINING_CAPEX (Catastro de inversiones mineras), CHILE_COPPER_EXPORTS (Exportaciones mineras valor FOB), CHILE_ELECTRICITY_DEMAND (Generación y demanda SEN vía Coordinador Eléctrico Nacional / INE).
   - *Confiabilidad*: 98.5% (Boletines e indicadores oficiales sectoriales).

---

## 5. Esquema Inicial de Base de Datos PostgreSQL

El esquema implementa un modelo de datos temporal normalizado con soporte para TimescaleDB / hypertables y JSONB para metadatos auditables:

1. `sources`: Catálogo de proveedores, URLs, confiabilidad y frecuencia.
2. `indicators`: Diccionario maestro de 30 variables fundamentales (código, nombre, categoría, unidad, dirección, source_id).
3. `observations`: Serie temporal de valores observados (`indicator_id`, `timestamp`, `value`, `quality_status`, `metadata`).
4. `derived_indicators`: Fórmulas y definiciones de métricas compuestas y transformadas.
5. `signals`: Detección de cambios de tendencia, quiebres de medias móviles, anomalías estadísticas.
6. `scores`: Valores cuantitativos de los 5 índices principales con `methodology_version` y desglose JSONB.
7. `regimes`: Registro de clasificación del régimen económico mundial.
8. `scenarios`: Estimaciones de probabilidad para los 4 escenarios macro (S1 a S4).
9. `transmission_channels`: Matriz de relaciones causa-efecto global → Chile.
10. `alerts`: Motor de alertas activas e históricas con umbrales y estado de resolución.
11. `ingestion_runs`: Observabilidad completa de ejecuciones del pipeline de datos.
12. `research_documents`: Capa de documentos de investigación económica para futura integración RAG.
