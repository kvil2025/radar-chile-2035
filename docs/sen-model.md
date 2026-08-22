# MODELO DEL SISTEMA ELÉCTRICO NACIONAL (SEN) — CHILE 2035

## 1. Estructura y Zonas del SEN

El Sistema Eléctrico Nacional (SEN) abarca más de 3.100 km desde Arica (Región de Arica y Parinacota) hasta la Isla Grande de Chiloé (Región de Los Lagos), abasteciendo a más del 99% de la población de Chile y la casi totalidad del consumo minero e industrial.

### Zonas Eléctricas Principales:
1. **Norte Grande (Arica a Antofagasta)**:
   - Características: Altísima radiación solar (DNI > 3.000 kWh/m²/año), concentración minera masiva de cobre y litio, proyectos de desalación.
   - Barras clave: `CRUCERO_220`, `KIMAL_500`, `ENCUENTRO_220`, `LABERINTO_220`, `ATACAMA_220`.
   - Dinámica: Fuerte sobreoferta solar al mediodía (riesgo de precio cero y curtailment), alta demanda nocturna minera (oportunidad masiva para BESS de 4 a 8 horas).
2. **Norte Chico (Atacama y Coquimbo)**:
   - Características: Transición solar y eólica (vientos costeros constantes).
   - Barras clave: `CARDONES_500`, `MAITENCILLO_500`, `PAN_DE_AZUCAR_220`.
   - Dinámica: Histórico cuello de botella de transmisión hacia el centro del país (Cardones-Polpaico 500 kV).
3. **Centro (Valparaíso, Metropolitana, O'Higgins, Maule)**:
   - Características: Mayor centro de consumo urbano, industrial y data centers (Santiago / Quilicura / Lampa).
   - Barras clave: `POLPAICO_500`, `LO_AGUIRRE_500`, `CERRO_NAVIA_220`, `ALTO_JAHUEL_500`, `ANCOA_500`.
   - Dinámica: Precios marginales más elevados en horas punta y noche; destino final de la futura línea HVDC Kimal-Lo Aguirre (~2029-2030).
4. **Sur (Ñuble, Biobío, Araucanía, Los Ríos, Los Lagos)**:
   - Características: Hidroelectricidad de embalse y pasada (Cuencas del Laja, Biobío, Maule), generación eólica y biomasa.
   - Barras clave: `CHARRUA_500`, `CONCEPCION_220`, `TEMUCO_220`, `PUERTO_MONTT_220`.
   - Dinámica: Gran estacionalidad hidrológica (año seco vs. año húmedo).

---

## 2. Parámetros Clave de Infraestructura

- **Voltajes Troncales**: 500 kV (Carretera eléctrica principal), 220 kV (Red troncal y zonal), 110/154/66 kV (Distribución y conexión local).
- **Líneas Troncales Críticas**:
  - `Cardones - Polpaico 500 kV` (Capacidad ~1.700 MW).
  - `Kimal - Lo Aguirre HVDC 500 kV` (En desarrollo, 3.000 MW, COD ~2029-2030).
  - `Crucero - Encuentro 220 kV` (Corredor minero).
  - `Ancoa - Alto Jahuel 500 kV` (Corredor hidro hacia el centro).

---

## 3. Modelo de Precios y Captura

1. **Costo Marginal Instantáneo ($/MWh)**: Costo de la unidad más cara en operar para satisfacer el siguiente MW de demanda en cada barra del sistema.
2. **Precio de Captura Solar**:
   $$P_{\text{captura, solar}} = \frac{\sum_{t=1}^{8760} P_t \times G_{\text{solar}, t}}{\sum_{t=1}^{8760} G_{\text{solar}, t}}$$
3. **Factor de Captura (Capture Rate)**:
   $$\text{Capture Rate} = \frac{P_{\text{captura}}}{P_{\text{promedio barra}}}$$
4. **Arbitraje BESS**:
   $$\text{Ingreso BESS} = \sum_{t \in \text{descarga}} P_t \times E_t \times \eta - \sum_{t \in \text{carga}} P_t \times E_t$$
   *(donde $\eta \approx 85\%$ es la eficiencia Round-Trip de ciclo completo)*.
