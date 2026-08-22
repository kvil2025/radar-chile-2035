from typing import Generator
from fastapi import Header, HTTPException, status
from sqlalchemy.orm import Session
from packages.common.database import SessionLocal
from packages.common.config import settings

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_api_key(x_api_key: str = Header(default=None)) -> bool:
    """Optional security check for administrative mutation endpoints."""
    if not settings.DEBUG:
        if not x_api_key or x_api_key != settings.API_SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API key."
            )
    return True
