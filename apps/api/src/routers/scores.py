from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from packages.common.models import Score
from packages.common.schemas import ScoreResponse
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/scores", tags=["Scores"])

SCORE_TYPES = [
    "CHILE_OPPORTUNITY",
    "MINING_CYCLE",
    "COMMODITY_CYCLE",
    "MONETARY_STRESS",
    "DOLLAR_STRESS"
]

@router.get("", response_model=list[ScoreResponse])
def get_latest_scores(db: Session = Depends(get_db)):
    """Retrieve the most recent calculated scores across all 5 strategic indices with explainability breakdown."""
    results = []
    for stype in SCORE_TYPES:
        latest = db.query(Score).filter(
            Score.score_type == stype
        ).order_by(Score.timestamp.desc()).first()

        if latest:
            meta = latest.metadata_json or {}
            results.append(ScoreResponse(
                id=latest.id,
                score_type=latest.score_type,
                timestamp=latest.timestamp,
                value=latest.value,
                confidence=latest.confidence,
                methodology_version=latest.methodology_version,
                metadata_json=meta,
                contributors=meta.get("contributors", []),
                trend=meta.get("trend", "STABLE"),
                delta_30d=meta.get("delta_30d", 0.0)
            ))

    return results

@router.get("/{score_type}", response_model=ScoreResponse)
def get_score_by_type(score_type: str, db: Session = Depends(get_db)):
    """Retrieve in-depth mathematical explainability and historical score for a specific index type."""
    normalized_type = score_type.upper()
    latest = db.query(Score).filter(
        Score.score_type == normalized_type
    ).order_by(Score.timestamp.desc()).first()

    if not latest:
        raise HTTPException(status_code=404, detail=f"Score type '{score_type}' not found.")

    meta = latest.metadata_json or {}
    return ScoreResponse(
        id=latest.id,
        score_type=latest.score_type,
        timestamp=latest.timestamp,
        value=latest.value,
        confidence=latest.confidence,
        methodology_version=latest.methodology_version,
        metadata_json=meta,
        contributors=meta.get("contributors", []),
        trend=meta.get("trend", "STABLE"),
        delta_30d=meta.get("delta_30d", 0.0)
    )
