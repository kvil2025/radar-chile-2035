# RADAR CHILE 2035 — Metodología de Scoring (Scoring v0.1)

## 1. Principios Cuantitativos
- Rango estandarizado: **0 a 100**.
- **Versión de Metodología**: `methodology_version = "v0.1"`.
- **Explicabilidad total**: Cada score reporta la suma ponderada de sus componentes con puntos exactos aportados ($C_i$), baseline y dirección.
- **Score de Confianza ($0.0 - 1.0$)**: Penaliza automáticamente la falta de datos frescos o series con `quality_status != VALID`.

$$\text{Score} = \sum_{i=1}^n w_i \times \text{Norm}(X_i, \text{direction}_i, \text{baseline}_i, \sigma_i)$$

---

## 2. Los 5 Índices Estratégicos

### 1. Dollar Stress Index (0-100)
Mide la presión de escasez/tensión de liquidez global del dólar y su costo.
- `DXY` (Peso 30%): Niveles > 105 aportan estrés elevado (+).
- `US10Y` (Peso 25%): Tasas altas incrementan costo de financiamiento en USD (+).
- `US30Y` (Peso 15%): Prima por plazo y presión en deuda larga (+).
- `US_CPI` (Peso 15%): Inflación pegajosa demora recortes de la Fed (+).
- `FOREIGN_TREASURY_HOLDINGS` (Peso 15%): Menor demanda extranjera de bonos del Tesoro incrementa tensión (+).

### 2. Monetary Stress Index (0-100)
Mide la fragilidad estructural del sistema monetario y fiscal global.
- `US_FISCAL_DEFICIT` + `US_DEBT` (Peso 30%): Dominancia fiscal (+).
- `GOLD` YoY & Tendencia (Peso 25%): Desdolarización y compra de bancos centrales (+).
- `Yield Curve Spread 10Y-2Y` (Peso 20%): Estrés de liquidez e inversión de curva (+).
- `USD_RESERVES_SHARE` (Peso 15%): Erosión de cuota de reserva global (+).
- `US_FED_RATE` (Peso 10%): Restricción de liquidez (+).

### 3. Commodity Cycle Index (0-100)
Evalúa si las materias primas están en ciclo de contracción, neutral o superciclo.
- `COPPER` (Peso 35%): Barómetro principal de electrificación y crecimiento (+).
- `OIL` (Peso 20%): Energía e inflación industrial (+).
- `GOLD` (Peso 15%): Cobertura monetaria (+).
- `IRON_ORE` (Peso 15%): Construcción y acero en Asia (+).
- `CHINA_PMI` (Peso 15%): Demanda fabril del mayor consumidor de commodities (+).

### 4. Mining Cycle Index (0-100)
Mide la salud operativa, de inversión y demanda del sector minero chileno y global.
- `COPPER` Precio Real (Peso 30%): Margen operacional (+).
- `CHILE_COPPER_PRODUCTION` (Peso 25%): Capacidad de oferta y leyes de mineral (+).
- `CHILE_MINING_CAPEX` (Peso 25%): Inversión en proyectos a 10 años (+).
- `CHINA_COPPER_IMPORTS` (Peso 20%): Tracción de demanda física (+).

### 5. Chile Opportunity Index (0-100)
Índice sintético del entorno económico de Chile. 0 = Máximo riesgo/contracción, 100 = Máxima oportunidad de expansión y atracción de inversiones.
- `COPPER` Momentum & Nivel (Peso 30%, Dirección +)
- `CHILE_MINING_CAPEX` & Exportaciones (Peso 20%, Dirección +)
- `CLP_USD` Estabilidad cambiaria (Peso 15%, Dirección + cuando el tipo de cambio es competitivo y sin volatilidad extrema)
- `CHILE_ELECTRICITY_DEMAND` & Demanda IA (Peso 15%, Dirección +)
- `CHILE_IMACEC` & Crecimiento (Peso 10%, Dirección +)
- `US10Y` / Tasa Externa (Peso 10%, Dirección - como viento en contra)
