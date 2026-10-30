import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from packages.common.config import settings
from packages.common.database import init_db
from apps.api.src.routers import (
    health, sources, indicators, observations, 
    scores, signals, regimes, scenarios, 
    chile_impact, alerts, research, pipeline, agents, energy, costo_marginal
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
app.include_router(regimes.router_singular)
app.include_router(scenarios.router)
app.include_router(chile_impact.router)
app.include_router(alerts.router)
app.include_router(research.router)
app.include_router(pipeline.router)
app.include_router(agents.router)
app.include_router(energy.router)
app.include_router(costo_marginal.router)

# Mount Frontend SPA if dist folder exists (Unified Docker / Railway / Cloud Run mode)
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

DIST_DIR = Path(__file__).resolve().parent.parent.parent.parent / "apps" / "web" / "dist"

if DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = DIST_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(DIST_DIR / "index.html")
else:
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
