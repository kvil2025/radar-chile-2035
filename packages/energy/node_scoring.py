from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from packages.common.models import Bus, NodeOpportunityScore, ProjectPipeline
from packages.energy.market_engine import EnergyMarketEngine
from packages.scoring.normalizers import normalize_min_max

class NodeScoringEngine:
    """
    Computes the Node Opportunity Score v0.1 for every electrical bus in the SEN.
    Provides transparent mathematical attribution and recommendation levels.
    """

    def __init__(self, db: Session):
        self.db = db
        self.market_engine = EnergyMarketEngine(db=db)

    def calculate_all_scores(self) -> List[NodeOpportunityScore]:
        """Compute and persist Node Opportunity Scores for all active buses."""
        buses = self.db.query(Bus).filter(Bus.status == "OPERATIONAL").all()
        scores = []

        for bus in buses:
            score_obj = self.calculate_bus_score(bus)
            scores.append(score_obj)

        self.db.commit()
        return scores

    def calculate_bus_score(self, bus: Bus) -> NodeOpportunityScore:
        """Calculate single bus score."""
        metrics = self.market_engine.calculate_bus_market_metrics(bus.id)
        
        # 1. Expected Price Score (Higher price is better for pure generation)
        exp_price_score = normalize_min_max(metrics["avg_price_usd_mwh"], 20.0, 100.0, direction=1)

        # 2. Solar Capture Score
        solar_cap_score = normalize_min_max(metrics["solar_capture_price"], 0.0, 80.0, direction=1)

        # 3. Wind Capture Score
        wind_cap_score = normalize_min_max(metrics["wind_capture_price"], 20.0, 90.0, direction=1)

        # 4. BESS Arbitrage Score (Larger peak-to-trough spread is better)
        bess_score = normalize_min_max(metrics["bess_arbitrage_spread"], 20.0, 120.0, direction=1)

        # 5. Curtailment & Congestion Risk (Higher score = LOWER risk / better grid flow)
        if bus.zone == "NORTE_GRANDE":
            curt_risk_score = 40.0  # High solar curtailment risk
            demand_score = 90.0     # Mining hub
            grid_score = 85.0       # Kimal HVDC origin
        elif bus.zone == "NORTE_CHICO":
            curt_risk_score = 55.0  # Cardones corridor
            demand_score = 65.0
            grid_score = 75.0
        elif bus.zone == "CENTRO":
            curt_risk_score = 92.0  # Minimal curtailment, high load center
            demand_score = 95.0     # Urban + Data centers
            grid_score = 88.0       # Reception hub
        else: # SUR
            curt_risk_score = 85.0
            demand_score = 68.0
            grid_score = 72.0

        # 6. Future Competition from Pipeline
        pipeline_count = self.db.query(ProjectPipeline).filter(ProjectPipeline.bus_id == bus.id).count()
        future_comp_score = max(20.0, 90.0 - (pipeline_count * 15.0))

        # Composite total score weighted by diversified attractiveness
        total_score = round(
            (bess_score * 0.25) +
            (solar_cap_score * 0.15) +
            (wind_cap_score * 0.10) +
            (exp_price_score * 0.15) +
            (demand_score * 0.15) +
            (curt_risk_score * 0.10) +
            (grid_score * 0.10),
            1
        )

        if total_score >= 80.0:
            rec = "HIGHLY_ATTRACTIVE"
        elif total_score >= 68.0:
            rec = "ATTRACTIVE"
        elif total_score >= 55.0:
            rec = "MODERATE"
        elif total_score >= 40.0:
            rec = "RISKY"
        else:
            rec = "AVOID"

        score_record = self.db.query(NodeOpportunityScore).filter(
            NodeOpportunityScore.bus_id == bus.id
        ).order_by(NodeOpportunityScore.timestamp.desc()).first()

        if not score_record:
            score_record = NodeOpportunityScore(bus_id=bus.id)
            self.db.add(score_record)

        score_record.total_score = total_score
        score_record.expected_price_score = round(exp_price_score, 1)
        score_record.capture_price_solar_score = round(solar_cap_score, 1)
        score_record.capture_price_wind_score = round(wind_cap_score, 1)
        score_record.bess_arbitrage_score = round(bess_score, 1)
        score_record.congestion_risk_score = round(curt_risk_score, 1)
        score_record.curtailment_risk_score = round(curt_risk_score, 1)
        score_record.future_competition_score = round(future_comp_score, 1)
        score_record.demand_growth_score = round(demand_score, 1)
        score_record.grid_expansion_score = round(grid_score, 1)
        score_record.recommendation_level = rec
        score_record.methodology_version = "v0.1"

        return score_record
