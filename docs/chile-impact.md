# RADAR CHILE 2035 — Motor de Transmisión a Chile (Chile Impact Engine)

## 1. Canales de Transmisión Macroeconómica

```text
                     ┌─────────────────────────────┐
                     │    VARIABLES GLOBALES       │
                     │  Tasas Fed / Cobre / China  │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │    CANALES DE TRANSMISIÓN   │
                     │ Financiero / Comercial / R. │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │      VARIABLES CHILE        │
                     │ CLP / TPM / Fisco / Minería │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │    IMPACTO CUANTITATIVO     │
                     │   Oportunidades & Riesgos   │
                     └─────────────────────────────┘
```

### Canal 1: Tasas Externas y Condiciones Financieras
- **Origen**: `US10Y` / `US_FED_RATE`
- **Mecanismo**: Aumento en diferencial de tasas externas atrae flujos hacia USD $\rightarrow$ Depreciación del `CLP_USD` $\rightarrow$ Presión inflacionaria importada en Chile (`CHILE_CPI`) $\rightarrow$ Banco Central de Chile limita recortes de `CHILE_TPM` $\rightarrow$ Costo del crédito doméstico más alto.

### Canal 2: Precio del Cobre y Finanzas Públicas
- **Origen**: `COPPER`
- **Mecanismo**: Cada centavo de dólar adicional promedio anual en el precio del cobre genera aproximadamente USD 25-30M en ingresos fiscales adicionales para el Estado de Chile (Codelco + Royalty Minero + Impuesto de Primera Categoría) $\rightarrow$ Mejora en `CHILE_FISCAL_BALANCE` $\rightarrow$ Menor prima por riesgo soberano (CDS Chile) $\rightarrow$ Estabilidad cambiaria.

### Canal 3: Demanda China y Sector Exportador
- **Origen**: `CHINA_PMI` / `CHINA_COPPER_IMPORTS`
- **Mecanismo**: Mayor dinamismo fabril chino $\rightarrow$ Crecimiento en `CHILE_COPPER_EXPORTS` $\rightarrow$ Mayor superávit comercial $\rightarrow$ Expansión del `CHILE_IMACEC` minero y servicios asociados.

### Canal 4: Infraestructura Tecnológica, Datacenters e Inteligencia Artificial
- **Origen**: `AI_DATA_CENTER_CAPEX_PROXY`
- **Mecanismo**: Demanda exponencial de cobre para transformadores, conductores y cableado de datacenters $\rightarrow$ Aceleración en `CHILE_MINING_CAPEX` $\rightarrow$ Incremento sostenido en `CHILE_ELECTRICITY_DEMAND` e impulso a proyectos de energía solar, eólica y almacenamiento en Chile.
