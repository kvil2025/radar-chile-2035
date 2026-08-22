# RADAR CHILE 2035 — Plan de Implementación Integral

**Versión**: 1.0  
**Fecha**: 2026-08-21  
**Autor**: Senior Staff Software Engineer & Quantitative Architect  

---

## 1. Visión y Principio Rector

RADAR CHILE 2035 es una plataforma cuantitativa de inteligencia económica diseñada bajo la regla de oro:
$$\text{DATA QUALITY} > \text{TRACEABILITY} > \text{CORRECTNESS} > \text{EXPLAINABILITY} > \text{ARCHITECTURE} > \text{ANALYTICS} > \text{UI} > \text{AI}$$

El sistema responde de manera continua y rigurosa a las tres preguntas clave:
1. **WHAT?** ¿Qué está ocurriendo en la economía mundial, monetaria y local?
2. **WHY?** ¿Qué componentes e indicadores explican este movimiento?
3. **SO WHAT?** ¿Cómo se transmite esto a Chile y qué riesgos u oportunidades genera?

---

## 2. Fases de Ejecución

### FASE 0: Arquitectura, Diagnóstico y Diseño de Esquema (Completado)
- Diagnóstico del entorno (`docs/current-state.md`).
- Documentación de arquitectura, modelo de datos y fuentes.
- Especificación formal del DDL PostgreSQL / TimescaleDB.

### FASE 1: Estructura del Monorepo y Base de Datos (SQLAlchemy 2.0 + Migraciones)
- Creación de la estructura del monorepo (`apps/api`, `apps/web`, `packages/*`, `workers/*`, `infrastructure/*`, `tests/*`, `docs/*`).
- Definición de modelos ORM tipados con SQLAlchemy 2.0 y soporte dual PostgreSQL / SQLite (para tests aislados).
- Inicialización de base de datos y scripts de migración Alembic.
- Carga de semillas (seeding) de las 30 variables maestras, fuentes de datos, escenarios base, canales de transmisión y reglas de alerta.

### FASE 2: Conectores de Ingesta Oficiales y Resilientes
- Arquitectura `BaseConnector` con rate limiting, retries exponenciales (httpx / tenacity), logging estructurado y fallbacks confiables.
- Implementación de conectores:
  - `FREDConnector`: Tasas US (10Y, 30Y, 2Y), FED Rate, Inflación CPI, Déficit Fiscal, Deuda y DXY.
  - `BancoCentralChileConnector`: Dólar Observado (CLP/USD), TPM, IPC Chile, IMACEC, PIB y Exportaciones Cobre.
  - `CommoditiesConnector`: Cobre (LME/COMEX), Oro, Petróleo Brent, Hierro y proxy Litio.
  - `WorldBankOECDConnector`: PMI China, Producción Industrial China, Reservas Globales USD.
  - `ChileSectorialConnector`: Producción de Cobre Mina (Cochilco), Inversión Minera (CAPEX), Demanda Eléctrica SEN.

### FASE 3: Motor de Validación y Calidad de Datos (Data Quality Engine)
- Validación de cada observación ingresada (`VALID`, `SUSPECT`, `MISSING`, `STALE`, `OUTLIER`, `INVALID`).
- Reglas de integridad: rango físico, coherencia de frecuencia, saltos porcentuales anómalos (>3 sigma), detección de timestamps duplicados o desfasados.
- Tabla `ingestion_runs` para trazabilidad completa de registros procesados, insertados, rechazados y tiempos de ejecución.

### FASE 4: Motor de Indicadores Derivados
- Transformaciones temporales: YoY (Year-over-Year), MoM (Month-over-Month), Medias Móviles (20d, 50d, 200d), Z-Scores móviles y Drawdowns.
- Indicadores financieros compuestos:
  - Spread de Curva de Rendimientos (US10Y - US2Y) y señal de inversión.
  - Tasas Reales (US10Y - US CPI YoY).
  - Ratios estructurales: Gold / Copper, Copper / Oil.

### FASE 5: Motor Cuantitativo de Scoring (Metodología v0.1)
- Normalización robusta (Z-score acotado y min-max con baselines históricos).
- Cálculo determinista y ponderado de los 5 índices estratégicos:
  1. **Dollar Stress Index** (0-100)
  2. **Monetary Stress Index** (0-100)
  3. **Commodity Cycle Index** (0-100)
  4. **Mining Cycle Index** (0-100)
  5. **Chile Opportunity Index** (0-100)
- Motor de Explicabilidad (WHY?): Desglose cuantitativo por puntos de contribución de cada componente, baseline, dirección y nivel de confianza.

### FASE 6: Clasificador de Régimen Económico Global
- Evaluación probabilística y basada en reglas sobre 8 regímenes:
  - `NORMAL`, `EXPANSION`, `TRANSITION`, `FISCAL_STRESS`, `INFLATIONARY`, `RECESSION`, `COMMODITY_SUPERCYCLE`, `MONETARY_STRESS`.
- Generación de síntesis institucional: *"Las condiciones actuales son consistentes con..."*.

### FASE 7: Motor de Escenarios Macroeconómicos
- Evaluación de los 4 escenarios canónicos:
  - **S1 — Soft Landing**
  - **S2 — Fiscal Dominance**
  - **S3 — Global Recession**
  - **S4 — Commodity Super Cycle**
- Cálculo de probabilidad (`probability_type = MODEL_ESTIMATE`), catalizadores activos, indicadores a favor/en contra, e impacto esperado en Chile.

### FASE 8: Motor de Transmisión a Chile y Sistema de Alertas
- **Chile Impact Engine**: Modelado de canales de transmisión macro (Tasas Fed → CLP → Inflación importada → TPM; Cobre → Royalty/Fisco → Inversión local; etc.).
- **Alert Engine**: Detección de umbrales críticos en tiempo real con severidades `INFO`, `WATCH`, `WARNING`, `CRITICAL` y tracking de resolución.

### FASE 9: Backend API (FastAPI)
- Arquitectura limpia con Pydantic v2 y endpoints REST estructurados:
  - `/health`, `/api/v1/sources`, `/api/v1/indicators`, `/api/v1/observations/{code}`, `/api/v1/scores`, `/api/v1/regime`, `/api/v1/scenarios`, `/api/v1/chile-impact`, `/api/v1/alerts`, `/api/v1/ingestion/run`.
- Documentación interactiva Swagger/OpenAPI en `/docs`.

### FASE 10: Workers y Automatización
- Pipeline de orquestación para ingesta diaria, recálculo semanal, evaluación de alertas y reconciliación de datos.

### FASE 11: Frontend Dashboard (Next.js 15 + Tailwind + Recharts + Design System Ávila Elgueta)
- Dark mode premium (`#0A0A0B`), Glassmorphism con bordes sutiles, paleta aprobada (Azul Marino `#0D2560`, Acento Naranja `#EF3800`, Dorado `#C9A84C`, Cyan `#00f2ff`).
- Header ejecutivo con Régimen Global activo y estado de confianza.
- 5 Macro Score Cards con tendencias, variaciones y modal interactivo de Explicabilidad ("WHY?").
- Paneles especializados: USA/Monetary, Commodities/Minería, Chile Real-Time, Escenarios Macroeconómicos, Matriz de Transmisión y Centro de Alertas.

### FASE 12: Suite de Testing Automatizado y Documentación
- Tests unitarios de fórmulas matemáticas y normalización.
- Tests de integración de endpoints FastAPI.
- Tests de calidad de datos (ausencia de duplicados, coherencia temporal, rangos).
- Documentación técnica exhaustiva en `docs/` y `walkthrough.md`.
