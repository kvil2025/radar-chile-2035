# RADAR CHILE 2035 — Arquitectura del Sistema

## 1. Principios de Diseño
1. **Clean Architecture & DDD**: Separación estricta entre capa de datos, dominio analítico, aplicación y presentación.
2. **Trazabilidad Absoluta**: Toda cifra mostrada en la plataforma tiene un origen auditable (fuente, URL, timestamp de ingestión, fórmula de transformación y versión metodológica).
3. **Idempotencia y Tolerancia a Fallos**: La re-ejecución de cualquier conector o motor de cálculo produce el mismo estado determinista sin duplicar datos ni degradar la base histórica.
4. **Explicabilidad Mandatoria (No Black Box)**: Ningún índice cuantitativo se emite sin su vector de contribución (`contributors`), baselines y nivel de confianza.

```
┌─────────────────────────────────────────────────────────────┐
│                    FUENTES DE DATOS                         │
│  FRED | Banco Central Chile | Commodities | WorldBank | INE │
└──────────────────────────────┬──────────────────────────────┘
                               │ (httpx, retries, backoff)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 INGESTA & DATA QUALITY                      │
│   Quality Validator: VALID / SUSPECT / OUTLIER / STALE      │
└──────────────────────────────┬──────────────────────────────┘
                               │ (SQLAlchemy ORM)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                ALMACENAMIENTO TEMPORAL                      │
│       PostgreSQL (TimescaleDB / JSONB Metadata)             │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌──────────────────────────────┐    ┌──────────────────────────────┐
│    INDICADORES DERIVADOS     │    │      SEÑALES & ALERTAS       │
│ YoY / MoM / Spreads / Z-Score│    │ Cruces, Inversiones, Umbral  │
└──────────────┬───────────────┘    └──────────────┬───────────────┘
               │                                   │
               ▼                                   │
┌──────────────────────────────┐                   │
│      MOTOR DE SCORING        │                   │
│  Dollar/Monetary/Commodity/  │                   │
│  Mining/Chile Opportunity    │                   │
└──────────────┬───────────────┘                   │
               │                                   │
        ┌──────┴───────────────┐                   │
        ▼                      ▼                   │
┌────────────────┐   ┌────────────────────┐        │
│ CLASIFICADOR   │   │ MOTOR DE           │        │
│ DE REGÍMENES   │   │ ESCENARIOS (S1-S4) │        │
└───────┬────────┘   └─────────┬──────────┘        │
        │                      │                   │
        └──────────────┬───────┘                   │
                       ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 MOTOR DE TRANSMISIÓN A CHILE                │
│       Canales Macro Global ──► Transmisión ──► Chile        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                        │
│          REST API / OpenAPI / Pydantic v2 Schemas           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 RADAR CHILE 2035 WEB UI                     │
│    Next.js 15 / React 19 / Tailwind / Recharts / Dark Luxe  │
└─────────────────────────────────────────────────────────────┘
```
