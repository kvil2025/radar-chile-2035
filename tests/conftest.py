import pytest
from fastapi.testclient import TestClient
from packages.common.database import Base, engine, SessionLocal, get_db
from apps.api.src.main import app
from scripts.seed_data import seed_database
from scripts.run_pipeline import run_full_pipeline

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Ensure tables and baseline data exist in database
    seed_database()
    run_full_pipeline()
    yield

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
