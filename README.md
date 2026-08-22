# RADAR CHILE 2035 — Plataforma Cuantitativa de Inteligencia Macroeconómica

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3128/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6.svg)](https://www.typescriptlang.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC.svg)](https://tailwindcss.com)
[![Tests](https://img.shields.io/badge/Tests-26%20Passed-brightgreen.svg)]()

> **RADAR CHILE 2035** es una plataforma cuantitativa de inteligencia económica diseñada para monitorear variables macroeconómicas globales, del sistema monetario, commodities, minería, energía, tecnología/IA y la economía chilena, respondiendo continuamente a tres preguntas:
> 1. **WHAT?** ¿Qué está ocurriendo?
> 2. **WHY?** ¿Qué componentes e indicadores explican este movimiento?
> 3. **SO WHAT?** ¿Cómo se transmite esto a Chile y qué riesgos u oportunidades genera?

---

## 🏛️ Principio Fundamental de Datos

$$\text{DATA QUALITY} > \text{TRACEABILITY} > \text{CORRECTNESS} > \text{EXPLAINABILITY} > \text{ARCHITECTURE} > \text{ANALYTICS} > \text{UI} > \text{AI}$$

El sistema distingue estrictamente entre:
- **DATO OBSERVADO**: Registro empírico con fuente oficial y timestamp.
- **INDICADOR CALCULADO**: Transformaciones cuantitativas (YoY, MoM, Z-scores, spreads).
- **INTERPRETACIÓN**: Diagnóstico de régimen macroeconómico basado en reglas de evidencia.
- **ESCENARIO**: Modelos probabilísticos (S1-S4) etiquetados como `MODEL_ESTIMATE`.
- **ALERTA**: Detección de quiebre de umbrales cuantitativos.

---

## 📐 Arquitectura del Sistema

```text
FUENTES OFICIALES (FRED, Banco Central de Chile, Cochilco, World Bank, Feeds de Commodities)
   ↓
INGESTA & CONECTORES RESILIENTES (Retries con exponential backoff, rate limiting)
   ↓
DATA QUALITY ENGINE (VALID, SUSPECT, MISSING, STALE, OUTLIER, INVALID)
   ↓
STORAGE TEMPORAL (PostgreSQL / TimescaleDB / SQLite / JSONB)
   ↓
INDICADORES DERIVADOS & SEÑALES (Spreads, Tasas Reales, Ratios Gold/Copper)
   ↓
MOTOR DE SCORING v0.1 (Dollar Stress, Monetary Stress, Commodity, Mining, Chile Opportunity)
   ↓
CLASIFICADOR DE REGÍMENES (8 estados: COMMODITY_SUPERCYCLE, MONETARY_STRESS, etc.)
   ↓
MOTOR DE ESCENARIOS (S1 Soft Landing, S2 Fiscal Dom, S3 Recession, S4 Supercycle)
   ↓
CANALES DE TRANSMISIÓN A CHILE (Global Macro → Transmisión → Domestic Impact)
   ↓
CENTRO DE ALERTAS (Severidades INFO, WATCH, WARNING, CRITICAL)
   ↓
FASTAPI REST API (/sources, /indicators, /scores, /regime, /scenarios, /chile-impact, /alerts)
   ↓
WEB DASHBOARD (Next.js / Vite / React / TypeScript / Recharts / Dark Premium Glassmorphism)
```

---

## 🎯 Los 5 Índices Estratégicos (Metodología v0.1)

1. **Dollar Stress Index (0-100)**: Tensión de liquidez global en USD (`DXY`, `US10Y`, `US30Y`, `US_CPI`, `FOREIGN_TREASURY_HOLDINGS`).
2. **Monetary Stress Index (0-100)**: Fragilidad del sistema monetario y dominancia fiscal (`US_FISCAL_DEFICIT`, `US_DEBT`, `GOLD`, `US_FED_RATE`, `USD_RESERVES_SHARE`).
3. **Commodity Cycle Index (0-100)**: Tracción del ciclo de materias primas (`COPPER`, `GOLD`, `OIL`, `IRON_ORE`, `CHINA_PMI`).
4. **Mining Cycle Index (0-100)**: Salud del sector minero (`COPPER`, `CHILE_COPPER_PRODUCTION`, `CHILE_MINING_CAPEX`, `CHINA_COPPER_IMPORTS`).
5. **Chile Opportunity Index (0-100)**: Oportunidad económica para Chile (`COPPER`, `CHILE_MINING_CAPEX`, `CLP_USD`, `CHILE_ELECTRICITY_DEMAND`, `CHILE_IMACEC`, `US10Y`).

---

## 🚀 Inicio Rápido (Quickstart)

### 1. Requisitos Previos
- Python 3.12+
- Node.js 20+

### 2. Configuración y Ejecución Local
```bash
# 1. Clonar o ingresar al workspace
cd /Users/cavila/.gemini/antigravity/scratch/radar_chile

# 2. Instalar dependencias
source .venv/bin/activate
pip install -r requirements.txt
npm --prefix apps/web install

# 3. Inicializar base de datos y sembrar metadatos maestros
python scripts/seed_data.py

# 4. Ejecutar pipeline completo de datos y scoring
python scripts/run_pipeline.py

# 5. Ejecutar suite de pruebas (26 tests pasando al 100%)
pytest -v

# 6. Iniciar Servidor Backend FastAPI (Puerto 8000)
python -m uvicorn apps.api.src.main:app --host 0.0.0.0 --port 8000 --reload

# 7. Iniciar Dashboard Web React (Puerto 3000)
npm --prefix apps/web run dev
```

---

## 🐳 Ejecución con Docker Compose

```bash
docker-compose up -d --build
```
- Web Dashboard: `http://localhost:3000`
- FastAPI OpenAPI Docs: `http://localhost:8000/docs`
- PostgreSQL / TimescaleDB: `localhost:5432`

---

## 🧪 Suite de Testing Automatizado

```bash
pytest -v
```
- `tests/unit/test_quality_validator.py`: Validación de rangos físicos, anomalías y saltos anómalos.
- `tests/unit/test_transformations.py`: Fórmulas de YoY, MoM, medias móviles, z-scores y drawdowns.
- `tests/unit/test_scoring.py`: Suma de pesos, normalizadores y explicabilidad.
- `tests/unit/test_regimes_scenarios.py`: Reglas de regímenes y probabilidades `MODEL_ESTIMATE`.
- `tests/integration/test_api_endpoints.py`: Endpoints REST de FastAPI.
- `tests/data_quality/test_database_integrity.py`: Integridad temporal y ausencia de duplicados.

---

## 📚 Documentación Técnica Detallada

- [`docs/current-state.md`](docs/current-state.md): Diagnóstico del entorno y arquitectura.
- [`docs/implementation-plan.md`](docs/implementation-plan.md): Plan integral de fases.
- [`docs/architecture.md`](docs/architecture.md): Diagrama y especificación arquitectónica.
- [`docs/data-model.md`](docs/data-model.md): Esquema relacional y DDL de base de datos.
- [`docs/data-sources.md`](docs/data-sources.md): Catálogo de las 30 variables y fuentes oficiales.
- [`docs/indicators.md`](docs/indicators.md): Indicadores sintéticos y fórmulas.
- [`docs/scoring.md`](docs/scoring.md): Metodología de scoring y explicabilidad (WHY?).
- [`docs/regimes.md`](docs/regimes.md): Clasificador de 8 regímenes macroeconómicos.
- [`docs/scenarios.md`](docs/scenarios.md): Modelado de escenarios S1 a S4.
- [`docs/chile-impact.md`](docs/chile-impact.md): Canales de transmisión macro global hacia Chile.
- [`docs/roadmap.md`](docs/roadmap.md): Hoja de ruta de evolución hacia agentes IA.
