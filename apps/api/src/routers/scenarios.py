from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.common.models import Scenario
from packages.common.schemas import ScenarioResponse
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/scenarios", tags=["Scenarios"])

@router.get("", response_model=list[ScenarioResponse])
def list_scenarios(db: Session = Depends(get_db)):
    """Retrieve the 4 canonical macro scenarios with updated MODEL_ESTIMATE probabilities."""
    return db.query(Scenario).order_by(Scenario.scenario_code.asc()).all()
