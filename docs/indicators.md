# RADAR CHILE 2035 — Indicadores Derivados (Indicators)

## 1. Transformaciones Temporales
Para cada serie temporal se calculan dinámicamente:
- **YoY (Year-over-Year %)**: $\frac{P_t - P_{t-N_{year}}}{P_{t-N_{year}}} \times 100$
- **MoM (Month-over-Month %)**: $\frac{P_t - P_{t-N_{month}}}{P_{t-N_{month}}} \times 100$
- **Rolling Averages (MA)**: 20 días (corto plazo), 50 días (medio plazo), 200 días (largo plazo).
- **Z-Score Móvil**: $Z_t = \frac{X_t - \mu_{rolling}}{\sigma_{rolling}}$ (Ventana 252 días hábiles / 1 año).
- **Drawdown**: $\frac{P_t - \max_{s \le t}(P_s)}{\max_{s \le t}(P_s)} \times 100$

---

## 2. Indicadores Sintéticos de Mercado

1. **Yield Curve Spread (10Y - 2Y)**:
   $$\text{Spread}_{10-2} = \text{US10Y} - \text{US2Y}$$
   - *Señal*: Inversión ($\text{Spread} < 0$) precede recesiones en EE.UU. La desinversión abrupta tras ciclo restrictivo anticipa aceleración de recortes o relajación de liquidez.

2. **US Real Rate**:
   $$\text{RealRate}_{10Y} = \text{US10Y} - \text{US\_CPI}$$
   - *Impacto*: Tasas reales altas encarecen el costo de capital global y presionan monedas emergentes como el peso chileno (CLP).

3. **Gold / Copper Ratio**:
   $$\text{Ratio}_{\text{Gold/Copper}} = \frac{\text{GOLD (USD/oz)}}{\text{COPPER (USD/lb)} \times 100}$$
   - *Significado*: Oro = activo de refugio / riesgo sistémico; Cobre = barómetro de crecimiento global e industrial. Un ratio alcista indica aversión al riesgo y desaceleración; un ratio a la baja indica ciclo expansivo/reflacionario.

4. **Copper / Oil Ratio**:
   $$\text{Ratio}_{\text{Copper/Oil}} = \frac{\text{COPPER (USD/lb)}}{\text{OIL (USD/bbl)}}$$
   - *Impacto en Chile*: Chile exporta cobre e importa petróleo. Un ratio alto representa una mejora masiva en los términos de intercambio de la economía chilena.
