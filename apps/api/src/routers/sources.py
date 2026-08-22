from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.common.models import Source
from packages.common.schemas import SourceResponse
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/sources", tags=["Sources"])

@router.get("", response_model=list[SourceResponse])
def list_sources(db: Session = Depends(get_db)):
    """List all registered official data sources and institutions."""
    return db.query(Source).order_by(Source.id.asc()).all()
