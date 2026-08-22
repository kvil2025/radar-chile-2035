# RADAR CHILE 2035 — Fuentes de Datos (Data Sources)

## 1. Catálogo Oficial de Fuentes

| Fuente | Proveedor | Tipo de Acceso | Frecuencia | Variables Principales | Confiabilidad |
|--------|-----------|----------------|------------|-----------------------|---------------|
| **FRED** | Federal Reserve Bank of St. Louis | REST API | Diaria / Mensual | US10Y, US30Y, US2Y, US_CPI, US_FED_RATE, US_FISCAL_DEFICIT, US_DEBT, DXY | 99.9% |
| **Banco Central de Chile** | BCCh Estadísticas / SIEL | API Oficial / Series REST | Diaria / Mensual / Trimestral | CLP_USD, CHILE_TPM, CHILE_CPI, CHILE_IMACEC, CHILE_GDP, CHILE_COPPER_EXPORTS | 99.5% |
| **Global Commodities & Financials** | Yahoo Finance / Stooq / Metals | REST / Market Feeds | Diaria (Cierre de mercado) | COPPER, GOLD, OIL, LITHIUM, IRON_ORE | 99.0% |
| **World Bank & OECD** | World Bank Open Data / OECD API | REST API | Mensual / Trimestral | CHINA_PMI, CHINA_INDUSTRIAL_PRODUCTION, USD_RESERVES_SHARE, FOREIGN_TREASURY_HOLDINGS | 99.0% |
| **Cochilco & INE Chile** | Cochilco / INE / CEN | Series Sectoriales / API Open Data | Mensual | CHILE_COPPER_PRODUCTION, CHILE_MINING_CAPEX, CHILE_ELECTRICITY_DEMAND, AI_DATA_CENTER_CAPEX_PROXY | 98.5% |

---

## 2. Las 30 Variables Iniciales

### A. Estados Unidos / Macro
1. `US10Y`: US 10-Year Treasury Yield (`%`, Diaria, FRED `DGS10`)
2. `US30Y`: US 30-Year Treasury Yield (`%`, Diaria, FRED `DGS30`)
3. `US2Y`: US 2-Year Treasury Yield (`%`, Diaria, FRED `DGS2`)
4. `US_CPI`: US Consumer Price Index YoY (`%`, Mensual, FRED `CPIAUCSL`)
5. `US_FED_RATE`: Federal Funds Effective Rate (`%`, Diaria/Mensual, FRED `FEDFUNDS`)
6. `US_FISCAL_DEFICIT`: US Federal Surplus or Deficit (% of GDP, Trimestral/Anual, FRED `FYFSD`)
7. `US_DEBT`: US Total Public Debt as % of GDP (`%`, Trimestral, FRED `GFDEGDQ188S`)

### B. Sistema Monetario
8. `DXY`: US Dollar Index (Nominal Trade-Weighted, Diaria, FRED `DTWEXAFEGS`)
9. `USD_RESERVES_SHARE`: Global Allocated FX Reserves in USD (`%`, Trimestral, IMF COFER)
10. `FOREIGN_TREASURY_HOLDINGS`: Foreign Holdings of U.S. Securities (`Trillion USD`, Mensual, US Treasury TIC / FRED)
11. `CENTRAL_BANK_GOLD`: Global Central Bank Gold Net Purchases (`Tonnes`, Trimestral, World Gold Council)

### C. Commodities
12. `COPPER`: Copper Futures LME/COMEX (`USD/lb`, Diaria, Market Feed `HG=F`)
13. `GOLD`: Gold Spot/Futures (`USD/troy oz`, Diaria, Market Feed `GC=F`)
14. `OIL`: Brent Crude Oil (`USD/bbl`, Diaria, Market Feed `BZ=F`)
15. `LITHIUM`: Lithium Carbonate Battery Grade Spot (`USD/tonne`, Semanal, Fastmarkets/Benchmark proxy)
16. `IRON_ORE`: Iron Ore 62% Fe CFR China (`USD/dmt`, Diaria, Market Feed `TIO=F`)

### D. China / Demanda Mundial
17. `CHINA_PMI`: China NBS Manufacturing PMI (`Index >50 expansion`, Mensual, NBS/World Bank)
18. `CHINA_INDUSTRIAL_PRODUCTION`: China Industrial Output YoY (`%`, Mensual, NBS)
19. `CHINA_COPPER_IMPORTS`: China Unwrought Copper & Products Imports (`Tonnes / YoY %`, Mensual, General Admin of Customs)

### E. Chile
20. `CLP_USD`: Tipo de Cambio Dólar Observado (`CLP/USD`, Diaria, Banco Central de Chile)
21. `CHILE_TPM`: Tasa de Política Monetaria (`%`, Diaria, Banco Central de Chile)
22. `CHILE_CPI`: Inflación IPC Chile YoY (`%`, Mensual, INE / Banco Central de Chile)
23. `CHILE_IMACEC`: Índice Mensual de Actividad Económica YoY (`%`, Mensual, Banco Central de Chile)
24. `CHILE_GDP`: PIB Real Chile YoY (`%`, Trimestral, Banco Central de Chile)
25. `CHILE_FISCAL_BALANCE`: Balance Fiscal Efectivo (% del PIB, Trimestral/Anual, DIPRES)

### F. Minería
26. `CHILE_COPPER_PRODUCTION`: Producción Nacional de Cobre Mina (`Miles TMF`, Mensual, Cochilco / INE)
27. `CHILE_MINING_CAPEX`: Catastro Inversión Minera 10 años (`Billion USD`, Trimestral/Anual, Cochilco)
28. `CHILE_COPPER_EXPORTS`: Exportaciones de Cobre Valor FOB (`Million USD`, Mensual, Banco Central de Chile)

### G. Energía / Tecnología
29. `CHILE_ELECTRICITY_DEMAND`: Demanda / Generación Bruta Sistema Eléctrico Nacional (`GWh`, Mensual, CEN / INE)
30. `AI_DATA_CENTER_CAPEX_PROXY`: Global Hyperscaler & AI Infrastructure CAPEX Growth (`% YoY`, Trimestral, SEC Filings / Market proxy)
