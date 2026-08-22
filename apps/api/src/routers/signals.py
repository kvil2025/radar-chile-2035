import datetime
from typing import Optional, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from packages.common.models import Signal
from packages.common.schemas import SchemaBase
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/signals", tags=["Signals"])

class SignalResponse(SchemaBase):
    id: int
    indicator_id: int
    timestamp: datetime.datetime
    signal_type: str
    signal_strength: float
    value: float
    baseline: Optional[float] = None
    metadata_json: Optional[dict[str, Any]] = None

@router.get("", response_model=list[SignalResponse])
def list_signals(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """List recent quantitative signals (inversions, z-score shocks, technical thresholds)."""
    return db.query(Signal).order_by(Signal.timestamp.desc()).limit(limit).all()
