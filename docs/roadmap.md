# RADAR CHILE 2035 — Roadmap de Desarrollo

## Fase 0: Arquitectura & Diseño (Completada)
- [x] Diagnóstico de arquitectura y entorno (`docs/current-state.md`)
- [x] Plan de implementación integral (`docs/implementation-plan.md`)
- [x] Especificación de modelo de datos (`docs/data-model.md`)
- [x] Catálogo de fuentes y 30 variables (`docs/data-sources.md`)
- [x] Especificación cuantitativa de indicadores, scoring, regímenes, escenarios e impacto Chile

## Fase 1: Base de Datos & Modelos (En Ejecución)
- [ ] Estructura completa del monorepo
- [ ] Modelos SQLAlchemy 2.0 y soporte dual PostgreSQL / SQLite
- [ ] Migraciones Alembic y DDL inicial
- [ ] Script de siembra (seed) de variables, fuentes, escenarios y alertas

## Fase 2: Conectores de Ingesta
- [ ] BaseConnector con reintentos y rate limiting
- [ ] Conectores para FRED, Banco Central, Commodities, World Bank, INE/Cochilco

## Fase 3: Data Quality Engine
- [ ] Validador de observaciones (VALID, SUSPECT, OUTLIER, STALE, etc.)
- [ ] Observabilidad del pipeline (`ingestion_runs`)

## Fase 4: Indicadores Derivados
- [ ] Transformaciones YoY, MoM, rolling stats, z-scores, yield spreads, ratios

## Fase 5: Motor Cuantitativo de Scoring
- [ ] Normalización robusta y cálculo de los 5 índices estratégicos
- [ ] Explicabilidad detallada por componentes (WHY?) y versionado `v0.1`

## Fase 6: Clasificador de Regímenes
- [ ] Evaluación de 8 regímenes económicos y generación de síntesis institucional

## Fase 7: Motor de Escenarios
- [ ] Modelado de S1 a S4 con probabilidades `MODEL_ESTIMATE`

## Fase 8: Transmisión Chile & Alertas
- [ ] Canales de transmisión macro global a variables chilenas
- [ ] Motor de alertas configurables por severidad

## Fase 9: API Backend FastAPI
- [ ] Endpoints REST documentados en OpenAPI / Swagger

## Fase 10: Workers & Orquestación
- [ ] Tareas de ingesta, recálculo y evaluación periódica

## Fase 11: Web Frontend
- [ ] Dashboard Next.js 15 / React / TypeScript / Recharts con Design System Ávila Elgueta

## Fase 12: Testing & Verificación
- [ ] Suite completa de tests unitarios, de integración y de calidad de datos
