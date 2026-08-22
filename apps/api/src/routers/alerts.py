from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from packages.common.models import Alert
from packages.common.schemas import AlertResponse
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/alerts", tags=["Alerts"])

@router.get("", response_model=list[AlertResponse])
def list_alerts(
    status: Optional[str] = Query(None, description="Filter by status: ACTIVE, ACKNOWLEDGED, RESOLVED"),
    severity: Optional[str] = Query(None, description="Filter by severity: INFO, WATCH, WARNING, CRITICAL"),
    db: Session = Depends(get_db)
):
    """Retrieve system alerts filtered by status or severity level."""
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status == status.upper())
    if severity:
        query = query.filter(Alert.severity == severity.upper())

    alerts = query.order_by(Alert.created_at.desc()).all()
    results = []
    for a in alerts:
        results.append(AlertResponse(
            id=a.id,
            severity=a.severity,
            title=a.title,
            description=a.description,
            indicator_id=a.indicator_id,
            indicator_code=a.indicator.code if a.indicator else None,
            trigger_value=a.trigger_value,
            current_value=a.current_value,
            status=a.status,
            created_at=a.created_at,
            resolved_at=a.resolved_at
        ))
    return results
