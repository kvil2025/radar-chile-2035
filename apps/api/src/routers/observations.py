import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from packages.common.models import Indicator, Observation
from packages.common.schemas import ObservationResponse
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/observations", tags=["Observations"])

@router.get("/{code}", response_model=list[ObservationResponse])
def get_observations_for_indicator(
    code: str,
    limit: int = Query(90, ge=1, le=1000, description="Number of observations to return"),
    start_date: Optional[datetime.date] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[datetime.date] = Query(None, description="End date filter (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Retrieve chronological series of verified empirical observations for a given indicator code."""
    ind = db.query(Indicator).filter(Indicator.code == code.upper()).first()
    if not ind:
        raise HTTPException(status_code=404, detail=f"Indicator '{code}' not found.")

    query = db.query(Observation).filter(Observation.indicator_id == ind.id)

    if start_date:
        query = query.filter(Observation.timestamp >= datetime.datetime.combine(start_date, datetime.time.min))
    if end_date:
        query = query.filter(Observation.timestamp <= datetime.datetime.combine(end_date, datetime.time.max))

    obs = query.order_by(Observation.timestamp.asc()).limit(limit).all()
    return obs
