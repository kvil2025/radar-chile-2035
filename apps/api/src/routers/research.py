from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.common.models import ResearchDocument
from packages.common.schemas import ResearchDocumentResponse
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/research", tags=["Research"])

@router.get("", response_model=list[ResearchDocumentResponse])
def list_research_documents(db: Session = Depends(get_db)):
    """Retrieve cataloged official research documents, reports, and central bank publications."""
    return db.query(ResearchDocument).order_by(ResearchDocument.published_at.desc()).all()
