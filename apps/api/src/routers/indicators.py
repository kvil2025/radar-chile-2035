from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from packages.common.models import Indicator, Observation
from packages.common.schemas import IndicatorResponse, IndicatorWithObservations
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/indicators", tags=["Indicators"])

@router.get("", response_model=list[IndicatorWithObservations])
def list_indicators(
    category: Optional[str] = Query(None, description="Filter by category (e.g. MACRO_USA, COMMODITIES, CHILE)"),
    db: Session = Depends(get_db)
):
    """List registered indicators with their latest observed value and metadata."""
    query = db.query(Indicator)
    if category:
        query = query.filter(Indicator.category == category)
    
    indicators = query.order_by(Indicator.id.asc()).all()
    results = []

    for ind in indicators:
        latest = db.query(Observation).filter(
            Observation.indicator_id == ind.id
        ).order_by(Observation.timestamp.desc()).first()

        prev = db.query(Observation).filter(
            Observation.indicator_id == ind.id
        ).order_by(Observation.timestamp.desc()).offset(1).first()

        mom_change = None
        if latest and prev and prev.value != 0:
            mom_change = round(((latest.value - prev.value) / abs(prev.value)) * 100.0, 2)

        results.append(IndicatorWithObservations(
            id=ind.id,
            code=ind.code,
            name=ind.name,
            description=ind.description,
            category=ind.category,
            unit=ind.unit,
            frequency=ind.frequency,
            direction=ind.direction,
            source_id=ind.source_id,
            created_at=ind.created_at,
            latest_value=latest.value if latest else None,
            latest_timestamp=latest.timestamp if latest else None,
            change_mom=mom_change
        ))

    return results

@router.get("/{code}", response_model=IndicatorWithObservations)
def get_indicator(code: str, db: Session = Depends(get_db)):
    """Retrieve detailed information and latest status for a specific indicator code."""
    ind = db.query(Indicator).filter(Indicator.code == code.upper()).first()
    if not ind:
        raise HTTPException(status_code=404, detail=f"Indicator '{code}' not found.")

    latest = db.query(Observation).filter(
        Observation.indicator_id == ind.id
    ).order_by(Observation.timestamp.desc()).first()

    return IndicatorWithObservations(
        id=ind.id,
        code=ind.code,
        name=ind.name,
        description=ind.description,
        category=ind.category,
        unit=ind.unit,
        frequency=ind.frequency,
        direction=ind.direction,
        source_id=ind.source_id,
        created_at=ind.created_at,
        latest_value=latest.value if latest else None,
        latest_timestamp=latest.timestamp if latest else None
    )
