from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.common.models import Regime
from packages.common.schemas import RegimeResponse
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/regimes", tags=["Regimes"])
router_singular = APIRouter(prefix="/api/v1/regime", tags=["Regimes"])

@router.get("", response_model=RegimeResponse)
@router.get("/current", response_model=RegimeResponse)
@router_singular.get("", response_model=RegimeResponse)
@router_singular.get("/current", response_model=RegimeResponse)
def get_current_regime(db: Session = Depends(get_db)):
    """Retrieve current global economic regime classification with empirical evidence and confidence."""
    latest = db.query(Regime).order_by(Regime.timestamp.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No regime classification found. Run pipeline first.")
    return latest
