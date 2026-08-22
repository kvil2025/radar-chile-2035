# ARQUITECTURA OBJETIVO — ENERGY & ECONOMIC INTELLIGENCE PLATFORM (CHILE 2035)

## 1. Visión del Sistema

La plataforma integra la inteligencia macroeconómica global y chilena con el modelado físico y económico del Sistema Eléctrico Nacional (SEN) para responder con trazabilidad matemática y económica a la localización óptima de inversiones en generación y almacenamiento de energía.

```text
                                GLOBAL RADAR & MACRO (FRED, WB, FX, Cu, Li, Brent)
                                                        │
                                                        ▼
                                       CHILE MACRO & DEMAND GROWTH (PIB, Minería, AI Data Centers)
                                                        │
                                                        ▼
                       ┌────────────────────────────────┴────────────────────────────────┐
                       ▼                                                                 ▼
         SEN PHYSICAL GRID TOPOLOGY                                         ENERGY MARKET & DISPATCH
     (Buses, Substations, Lines, Cap, kV)                              (Nodal Prices, Marginal Cost, Loss)
                       │                                                                 │
                       └────────────────────────────────┬────────────────────────────────┘
                                                        │
                                                        ▼
                                        PROJECTS & BESS PIPELINE (2026-2035)
                                    (Solar, Wind, BESS, Hydro, Transmission Kimal-Lo Aguirre)
                                                        │
                                                        ▼
                                  HYDROLOGY & CLIMATE (Basins, Inflows, Solar/Wind Resource)
                                                        │
                                                        ▼
                                         ENERGY QUANT & GRID ENGINE
                                (Capture Price, Curtailment, Congestion Index, Loss Factor)
                                                        │
                                                        ▼
                                       NODE OPPORTUNITY SCORING ENGINE (0-100)
                                (Expected Price, Volatility, Congestion, Curtailment, Demand)
                                                        │
                                                        ▼
                                      PROJECT SITING & FINANCIAL OPTIMIZER
                                     (NPV, IRR, LCOE, Payback, Ranking Top 10 Buses)
                                                        │
                                                        ▼
                                            FASTAPI REST API & DATA LINEAGE
                                                        │
                                                        ▼
                                      ENERGY DASHBOARD & GEOSPATIAL MAP (SEN)
                                                        │
                                                        ▼
                                       AI ENERGY ADVISOR (Gemini Grounded Reasoning)
```

---

## 2. Capas de la Plataforma

1. **Capa 1: Ingesta & Data Quality**:
   - Conectores con reintentos y timeouts hacia CEN (Coordinador Eléctrico Nacional), CNE, SEA y DGA.
   - Validador de rangos físicos: Precios nodales ($0 a $400 USD/MWh), Voltajes (110 a 500 kV), Factores de planta (0% a 100%), Curtailment (0% a 100%).
2. **Capa 2: Base de Datos Temporal y Geoespacial**:
   - Tablas maestras de infraestructura eléctrica, series temporales horarias, proyectos y scores.
3. **Capa 3: Modelado de Red y Mercado**:
   - Cálculo de precios de captura por tecnología (Solar, Eólica, BESS, Hidro).
   - Detección de desacoples zonales (Norte Grande, Norte Chico, Centro, Sur).
   - Factores de penalización por pérdidas y congestión de líneas de transmisión.
4. **Capa 4: Motor de Oportunidad y Evaluación de Inversiones**:
   - Score de Atractividad Nodal (0–100) para cada barra del SEN.
   - Simulador financiero de proyectos: Ingreso de Capacidad (MW), Almacenamiento (MWh), CAPEX/OPEX, COD (ej. 2029) y horizonte (25 años) -> Genera Flujo de Caja Proyectado, NPV e IRR.
5. **Capa 5: Presentación y AI Advisor**:
   - Dashboard interactivo con mapa de barras del SEN con código de colores, heatmap de precios nodales, ranking de oportunidad y evaluador de proyectos.
   - Agente asesor energético con fundamentación estricta en datos reales.
