import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from packages.common.config import settings
from packages.common.database import init_db
from apps.api.src.routers import (
    health, sources, indicators, observations, 
    scores, signals, regimes, scenarios, 
    chile_impact, alerts, research, pipeline
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("radar_chile.api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting RADAR CHILE 2035 API Server...")
    init_db()
    yield
    logger.info("🛑 Shutting down RADAR CHILE 2035 API Server...")

app = FastAPI(
    title="RADAR CHILE 2035 — Economic Intelligence API",
    description=(
        "Quantitative API for macroeconomic monitoring, commodities, monetary stress, "
        "regime classification, scenario modeling, and Chile transmission channels."
    ),
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all modular routers
app.include_router(health.router)
app.include_router(sources.router)
app.include_router(indicators.router)
app.include_router(observations.router)
app.include_router(scores.router)
app.include_router(signals.router)
app.include_router(regimes.router)
app.include_router(scenarios.router)
app.include_router(chile_impact.router)
app.include_router(alerts.router)
app.include_router(research.router)
app.include_router(pipeline.router)

@app.get("/")
def root():
    return {
        "project": "RADAR CHILE 2035",
        "description": "Plataforma de Inteligencia Cuantitativa y Transmisión Macroeconómica",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_url": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.src.main:app", host="0.0.0.0", port=8000, reload=True)
