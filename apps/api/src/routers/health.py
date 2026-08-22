import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from packages.common.schemas import SchemaBase
from packages.common.config import settings
from apps.api.src.dependencies import get_db

router = APIRouter(tags=["Health"])

class HealthResponse(SchemaBase):
    status: str
    version: str
    environment: str
    database: str
    timestamp: datetime.datetime

@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint confirming database connectivity and service state."""
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {e}"

    return HealthResponse(
        status="operational",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        database=db_status,
        timestamp=datetime.datetime.utcnow()
    )
