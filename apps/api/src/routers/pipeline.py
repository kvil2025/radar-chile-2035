from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from packages.common.models import IngestionRun
from packages.common.schemas import IngestionRunResponse
from packages.data.pipeline import IngestionPipeline
from packages.indicators.derived_engine import DerivedIndicatorsEngine
from packages.scoring.engine import ScoringEngine
from packages.scenarios.regimes import EconomicRegimeClassifier
from packages.scenarios.scenario_engine import ScenarioEngine
from packages.scenarios.chile_impact import ChileImpactEngine
from packages.scenarios.alerts import AlertEngine
from apps.api.src.dependencies import get_db, verify_api_key

router = APIRouter(prefix="/api/v1/pipeline", tags=["Pipeline & Ingestion"])

@router.get("/runs", response_model=list[IngestionRunResponse])
def list_ingestion_runs(limit: int = 20, db: Session = Depends(get_db)):
    """List recent ingestion execution logs with status and metrics."""
    return db.query(IngestionRun).order_by(IngestionRun.started_at.desc()).limit(limit).all()

@router.post("/ingest", response_model=dict)
def trigger_ingestion(
    background_tasks: BackgroundTasks,
    days_back: int = 60,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_api_key)
):
    """Trigger full data ingestion across all 5 official connectors."""
    pipeline = IngestionPipeline(db=db)
    runs = pipeline.run_all(days_back=days_back)
    return {
        "status": "completed",
        "connectors_run": len(runs),
        "total_inserted": sum(r.records_inserted for r in runs),
        "total_rejected": sum(r.records_rejected for r in runs)
    }

@router.post("/recalculate", response_model=dict)
def trigger_recalculation(
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_api_key)
):
    """Trigger recalculation of derived indicators, scoring models, regimes, scenarios, and alerts."""
    derived = DerivedIndicatorsEngine(db=db).run()
    scores = ScoringEngine(db=db).run_all()
    regime = EconomicRegimeClassifier(db=db).classify()
    scenarios = ScenarioEngine(db=db).evaluate_scenarios()
    chile_impact = ChileImpactEngine(db=db).evaluate_channels()
    alerts = AlertEngine(db=db).evaluate_alerts()

    return {
        "status": "success",
        "derived": derived,
        "scores": scores,
        "regime": regime["regime_code"],
        "scenarios_evaluated": len(scenarios),
        "net_opportunity_score": chile_impact["net_opportunity_score"],
        "active_alerts": len(alerts)
    }
