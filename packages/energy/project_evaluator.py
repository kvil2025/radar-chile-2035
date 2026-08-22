import numpy as np
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from packages.common.models import Bus, NodeOpportunityScore
from packages.common.schemas import ProjectEvaluationRequest, ProjectEvaluationResult, BusRankingItem
from packages.energy.market_engine import EnergyMarketEngine

def calc_npv(rate: float, values: List[float]) -> float:
    """Calculate Net Present Value using standard discounted cash flow formula."""
    return sum(v / ((1.0 + rate) ** t) for t, v in enumerate(values))

def calc_irr(values: List[float]) -> float:
    """Calculate Internal Rate of Return using binary search / secant method."""
    if len(values) < 2 or values[0] >= 0:
        return 0.0
    
    # Binary search for rate where NPV is ~0
    low, high = -0.5, 1.0
    for _ in range(100):
        mid = (low + high) / 2.0
        val = calc_npv(mid, values)
        if abs(val) < 1e-4:
            return mid
        if val > 0:
            low = mid
        else:
            high = mid
    return mid

class ProjectEvaluator:
    """
    Financial and technical project siting evaluator.
    Ranks electrical buses in Chile for Generation + BESS projects
    by calculating projected cash flows, NPV, IRR, LCOE, and payback.
    """

    def __init__(self, db: Session):
        self.db = db
        self.market_engine = EnergyMarketEngine(db=db)

    def evaluate_project(self, req: ProjectEvaluationRequest) -> ProjectEvaluationResult:
        # 1. Benchmark CAPEX & OPEX
        capex_solar = (req.capacity_mw * 0.72) if "SOLAR" in req.technology else 0.0
        capex_wind = (req.capacity_mw * 1.15) if "WIND" in req.technology else 0.0
        capex_bess = (req.storage_mwh * 0.24) if req.storage_mwh > 0 else 0.0
        
        total_capex = req.custom_capex_musd if req.custom_capex_musd is not None else round(capex_solar + capex_wind + capex_bess, 2)
        annual_opex = req.custom_opex_musd_year if req.custom_opex_musd_year is not None else round(total_capex * 0.018, 2)
        discount_rate = req.discount_rate_pct / 100.0

        buses = self.db.query(Bus).filter(Bus.status == "OPERATIONAL").all()
        ranked_buses: List[BusRankingItem] = []

        for bus in buses:
            metrics = self.market_engine.calculate_bus_market_metrics(bus.id)
            score_rec = self.db.query(NodeOpportunityScore).filter(
                NodeOpportunityScore.bus_id == bus.id
            ).order_by(NodeOpportunityScore.timestamp.desc()).first()

            opp_score = score_rec.total_score if score_rec else 50.0
            rec_level = score_rec.recommendation_level if score_rec else "MODERATE"

            # Regional Capacity Factor
            if bus.zone == "NORTE_GRANDE":
                cf_solar = 0.34
                cf_wind = 0.32
                curt_risk = "MODERADO (Alta absorción por BESS)" if req.storage_mwh > 0 else "ALTO (30% sin BESS)"
                cong_risk = "BAJO (Receptor Kimal HVDC 2029)"
            elif bus.zone == "NORTE_CHICO":
                cf_solar = 0.30
                cf_wind = 0.39
                curt_risk = "BAJO-MODERADO"
                cong_risk = "MODERADO"
            elif bus.zone == "CENTRO":
                cf_solar = 0.24
                cf_wind = 0.28
                curt_risk = "BAJO"
                cong_risk = "BAJO (Centro de carga)"
            else: # SUR
                cf_solar = 0.17
                cf_wind = 0.40
                curt_risk = "BAJO"
                cong_risk = "BAJO"

            # 25-Year Cash Flow Projection
            annual_gen_mwh = req.capacity_mw * 8760.0 * (cf_solar if "SOLAR" in req.technology else cf_wind)
            cash_flows = [-total_capex]
            total_discounted_gen = 0.0
            total_discounted_costs = total_capex

            # Price projections with slight long-term convergence
            base_solar_price = max(18.0, metrics["solar_capture_price"])
            base_wind_price = max(40.0, metrics["wind_capture_price"])
            bess_spread = max(35.0, metrics["bess_arbitrage_spread"])

            # If project enters after 2029 (Kimal-Lo Aguirre COD), northern prices recover
            if req.target_cod_year >= 2029 and bus.zone == "NORTE_GRANDE":
                base_solar_price = max(32.0, base_solar_price * 1.35)

            for year in range(1, req.lifetime_years + 1):
                deg_factor = (1.0 - 0.005) ** year  # 0.5% degradation per year
                bess_deg = (1.0 - 0.015) ** year   # 1.5% BESS degradation per year

                # Generation Revenue
                gen_rev_m = (annual_gen_mwh * deg_factor * (base_solar_price if "SOLAR" in req.technology else base_wind_price)) / 1e6
                
                # BESS Arbitrage Revenue: 350 cycles per year * storage * spread * efficiency
                bess_rev_m = (req.storage_mwh * 350.0 * bess_spread * bess_deg) / 1e6 if req.storage_mwh > 0 else 0.0
                
                gross_revenue = gen_rev_m + bess_rev_m
                net_cf = gross_revenue - annual_opex
                cash_flows.append(round(net_cf, 3))

                # For LCOE
                total_discounted_gen += (annual_gen_mwh * deg_factor) / ((1.0 + discount_rate) ** year)
                total_discounted_costs += annual_opex / ((1.0 + discount_rate) ** year)

            # Financial Metrics
            try:
                npv_val = round(float(calc_npv(discount_rate, cash_flows)), 2)
            except Exception:
                npv_val = 0.0

            try:
                irr_val = round(float(calc_irr(cash_flows)) * 100.0, 1)
            except Exception:
                irr_val = 0.0

            lcoe_val = round(total_discounted_costs * 1e6 / (total_discounted_gen + 1e-6), 1)

            # Payback calculation
            cum_cf = 0.0
            payback_years = float(req.lifetime_years)
            for y_idx, cf in enumerate(cash_flows[1:], start=1):
                cum_cf += cf
                if cum_cf >= total_capex:
                    payback_years = round(y_idx - (cum_cf - total_capex) / cf, 1)
                    break

            # Rationale Generator
            if req.storage_mwh > 0 and bus.zone in ["NORTE_GRANDE", "NORTE_CHICO"]:
                rationale = f"Excelente spread de arbitraje BESS (${bess_spread:.1f}/MWh) con alta radiación (CF {cf_solar*100:.0f}%). El almacenamiento valoriza la energía diurna en el bloque nocturno minero."
            elif bus.zone == "CENTRO":
                rationale = f"Mayor precio de captura solar/base (${base_solar_price:.1f}/MWh) y cercanía a centros de consumo/data centers. Riesgo de congestión prácticamente nulo."
            elif "WIND" in req.technology and bus.zone in ["NORTE_CHICO", "SUR"]:
                rationale = f"Alto factor de planta eólico (CF {cf_wind*100:.0f}%) con generación complementaria en horas punta y noche. Retorno financiero sólido."
            else:
                rationale = f"Condiciones operativas estables con precio promedio de ${metrics['avg_price_usd_mwh']:.1f}/MWh y demanda zonal sostenida."

            ranked_buses.append(BusRankingItem(
                rank=0,
                bus_id=bus.id,
                bus_code=bus.code,
                bus_name=bus.name,
                zone=bus.zone,
                region=bus.region,
                opportunity_score=opp_score,
                recommendation_level=rec_level,
                avg_price_usd_mwh=metrics["avg_price_usd_mwh"],
                capture_price_solar=metrics["solar_capture_price"],
                capture_price_wind=metrics["wind_capture_price"],
                bess_arbitrage_spread=metrics["bess_arbitrage_spread"],
                curtailment_risk=curt_risk,
                congestion_risk=cong_risk,
                npv_musd=npv_val,
                irr_pct=irr_val,
                lcoe_usd_mwh=lcoe_val,
                payback_years=payback_years,
                summary_rationale=rationale
            ))

        # Sort by NPV descending (or opportunity score)
        ranked_buses.sort(key=lambda x: (x.npv_musd, x.opportunity_score), reverse=True)

        for i, item in enumerate(ranked_buses[:10], start=1):
            item.rank = i

        import datetime
        return ProjectEvaluationResult(
            request=req,
            estimated_capex_musd=total_capex,
            estimated_opex_musd_year=annual_opex,
            top_buses_ranking=ranked_buses[:10],
            methodology="DCF_MODEL_v0.1_SEN_CHILE",
            timestamp=datetime.datetime.utcnow()
        )
