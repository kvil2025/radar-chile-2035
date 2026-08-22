import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "RADAR CHILE 2035"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./radar_chile.db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "radar_chile"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # External API Keys (read from environment / .env)
    FRED_API_KEY: str = ""
    BANCO_CENTRAL_USER: str = ""
    BANCO_CENTRAL_PASS: str = ""
    GEMINI_API_KEY: str = ""
    
    # Methodology
    DEFAULT_METHODOLOGY_VERSION: str = "v0.1"
    
    # API Security
    API_SECRET_KEY: str = "radar-chile-2035-secure-token-development-secret-key"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000", "*"]
    
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
