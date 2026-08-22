from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.common.models import TransmissionChannel
from packages.common.schemas import ChileImpactOverview, TransmissionChannelResponse
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/chile-impact", tags=["Chile Impact"])

@router.get("", response_model=ChileImpactOverview)
def get_chile_impact(db: Session = Depends(get_db)):
    """Retrieve transmission matrix and net opportunity score for Chile."""
    channels = db.query(TransmissionChannel).order_by(TransmissionChannel.current_impact_score.desc()).all()
    channel_res = [
        TransmissionChannelResponse(
            id=ch.id,
            channel_name=ch.channel_name,
            global_indicator_code=ch.global_indicator_code,
            chile_indicator_code=ch.chile_indicator_code,
            transmission_speed=ch.transmission_speed,
            elasticity=ch.elasticity,
            description=ch.description,
            current_impact_score=ch.current_impact_score,
            updated_at=ch.updated_at
        )
        for ch in channels
    ]

    net_score = round(sum(ch.current_impact_score for ch in channels) / max(1, len(channels)), 1)
    best_channel = channels[0].channel_name if channels else "N/A"
    worst_channel = channels[-1].channel_name if channels else "N/A"

    return ChileImpactOverview(
        net_opportunity_score=net_score,
        primary_positive_channel=best_channel,
        primary_risk_channel=worst_channel,
        channels=channel_res
    )
