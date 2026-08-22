import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.models import Indicator, Observation, Score, Regime
from packages.common.database import SessionLocal
from packages.agents.gemini_client import GeminiClient
from packages.scoring.normalizers import normalize_min_max

logger = logging.getLogger(__name__)

class StressTestingAgent:
    """
    Simulates macroeconomic shocks ('¿Qué pasa si...?') and calculates
    projected impacts on Chile's Opportunity Index, exchange rate (CLP/USD),
    fiscal revenue, and global regime transition.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()
        self.ai = GeminiClient()

    def simulate_shock(
        self,
        copper_price: float,
        us10y_yield: float,
        oil_price: float = 78.0,
        china_pmi: float = 50.5,
        dxy_index: float = 104.5
    ) -> dict:
        logger.info(
            f"🧪 Simulating Macro Shock: Copper=${copper_price}/lb, "
            f"US10Y={us10y_yield}%, Oil=${oil_price}/bbl, ChinaPMI={china_pmi}, DXY={dxy_index}"
        )

        # Baseline reference levels
        baseline_copper = 4.38
        baseline_us10y = 4.69
        baseline_clp = 932.50
        baseline_oil = 77.90

        # 1. Projected Exchange Rate (CLP/USD)
        # Elasticity: +100 bps in US10Y depreciates CLP by ~3.5%; +$0.50 in Copper appreciates CLP by ~4.0%
        us10y_diff = us10y_yield - baseline_us10y
        copper_diff = copper_price - baseline_copper

        clp_us10y_effect = us10y_diff * 35.0  # +$35 CLP per 100 bps US10Y
        clp_copper_effect = -copper_diff * 75.0  # -$75 CLP per $1.00/lb Copper

        projected_clp = round(max(700.0, min(1300.0, baseline_clp + clp_us10y_effect + clp_copper_effect)), 1)
        clp_delta = round(projected_clp - baseline_clp, 1)

        # 2. Projected Fiscal Revenue Impact (USD Millions per year)
        # Rule of thumb: each 10 cents of annual copper price delta impacts fiscal revenue by ~USD $280M
        fiscal_impact_usd_million = round((copper_price - baseline_copper) * 2800.0, 1)

        # 3. Recalculate Chile Opportunity Score under shock
        norm_copper = normalize_min_max(copper_price, 3.0, 5.50, direction=1)
        norm_capex = 65.0  # Baseline
        norm_clp = normalize_min_max(projected_clp, 780.0, 1050.0, direction=-1)
        norm_energy = 55.0
        norm_imacec = 50.0
        norm_us10y = normalize_min_max(us10y_yield, 2.5, 5.5, direction=-1)

        simulated_chile_opportunity = round(
            (norm_copper * 0.30) +
            (norm_capex * 0.20) +
            (norm_clp * 0.15) +
            (norm_energy * 0.15) +
            (norm_imacec * 0.10) +
            (norm_us10y * 0.10),
            1
        )

        # 4. Recalculate Dollar Stress Score under shock
        norm_dxy = normalize_min_max(dxy_index, 90.0, 115.0, direction=1)
        norm_us10y_stress = normalize_min_max(us10y_yield, 2.0, 6.0, direction=1)
        norm_us30y_stress = normalize_min_max(us10y_yield + 0.35, 2.5, 6.5, direction=1)
        simulated_dollar_stress = round(
            (norm_dxy * 0.30) + (norm_us10y_stress * 0.25) + (norm_us30y_stress * 0.15) + (55.0 * 0.15) + (50.0 * 0.15),
            1
        )

        # 5. Determine Simulated Regime
        if copper_price >= 4.50 and china_pmi >= 50.0:
            simulated_regime = "COMMODITY_SUPERCYCLE"
        elif us10y_yield >= 5.0 or dxy_index >= 108.0:
            simulated_regime = "MONETARY_STRESS"
        elif china_pmi < 48.5 or copper_price < 3.70:
            simulated_regime = "RECESSION"
        elif us10y_yield <= 3.80 and 4.0 <= copper_price <= 4.40:
            simulated_regime = "EXPANSION"
        else:
            simulated_regime = "TRANSITION"

        # 6. Generate AI Qualitative Simulation Assessment
        prompt = f"""Analiza el siguiente escenario de simulación de shock macroeconómico ('Stress Test') para Chile:
- Precio del Cobre Simulado: ${copper_price:.2f}/lb (Variación: {copper_diff:+.2f} USD/lb)
- Rendimiento Bono US10Y Simulado: {us10y_yield:.2f}% (Variación: {us10y_diff:+.2f}%)
- Petróleo Brent Simulado: ${oil_price:.1f}/bbl
- PMI Manufacturero China Simulado: {china_pmi:.1f}
- Índice Dólar DXY Simulado: {dxy_index:.1f}

Resultados Cuantitativos Modelados:
- Tipo de Cambio Proyectado: ${projected_clp:.1f} CLP/USD (Variación: {clp_delta:+.1f} pesos)
- Impacto Fiscal Estimado en Chile: {fiscal_impact_usd_million:+.1f} millones de USD
- Chile Opportunity Index Simulado: {simulated_chile_opportunity:.1f} / 100
- Dollar Stress Index Simulado: {simulated_dollar_stress:.1f} / 100
- Régimen Económico Resultante: {simulated_regime}

Entrega una evaluación ejecutiva concisa (max 250 palabras) explicando los mecanismos de transmisión y los principales riesgos u oportunidades para la economía chilena bajo este shock.
"""

        ai_analysis = self.ai.generate_content(
            system_instruction="Eres el motor cuantitativo de Stress Testing de RADAR CHILE 2035. Responde con rigurosidad cuantitativa, formato Markdown y lenguaje ejecutivo.",
            prompt=prompt
        )

        return {
            "inputs": {
                "copper_price_usd_lb": copper_price,
                "us10y_yield_pct": us10y_yield,
                "oil_price_usd_bbl": oil_price,
                "china_pmi": china_pmi,
                "dxy_index": dxy_index
            },
            "projections": {
                "projected_clp_usd": projected_clp,
                "clp_delta": clp_delta,
                "fiscal_impact_usd_million": fiscal_impact_usd_million,
                "simulated_chile_opportunity_score": simulated_chile_opportunity,
                "simulated_dollar_stress_score": simulated_dollar_stress,
                "simulated_regime": simulated_regime
            },
            "ai_assessment": ai_analysis,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    def close(self):
        if not self.db_provided:
            self.db.close()
        self.ai.close()
