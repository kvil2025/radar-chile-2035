import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from packages.common.config import settings

logger = logging.getLogger(__name__)

# Base declarative class
Base = declarative_base()

# Configure database engine
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency for obtaining a database session in FastAPI routers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """Initialize database tables."""
    import packages.common.models  # Ensure models are imported
    logger.info("Creating database tables if not exist...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
