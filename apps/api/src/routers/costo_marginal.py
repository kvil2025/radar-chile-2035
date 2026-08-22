from typing import Optional, Dict, Any
from fastapi import APIRouter, Query, Body
from packages.costo_marginal.ml_forecast_engine import MLForecastEngine
from packages.costo_marginal.climate_analytics import ClimateAnalyticsEngine
from packages.costo_marginal.regulatory_corpus import RegulatoryCorpusEngine
from packages.costo_marginal.cen_api_client import CoordinadorElectricoClient

router = APIRouter(prefix="/api/v1/costo-marginal", tags=["Marginal Cost Predictive Analytics & ML"])

forecast_engine = MLForecastEngine()
climate_engine = ClimateAnalyticsEngine()
cen_client = CoordinadorElectricoClient()

@router.get("/dataset-summary")
def get_dataset_summary():
    """Returns statistical summary and metrics of the 5-year historical marginal cost dataset."""
    return forecast_engine.get_dataset_summary()

@router.post("/train-predict")
def train_and_forecast(
    horizon_hours: int = Query(72, ge=12, le=168, description="Forecast horizon in hours (12 to 168)"),
    n_estimators: int = Query(60, ge=20, le=150, description="Number of trees in Random Forest")
):
    """
    Trains Random Forest Regressor on historical hourly data with harmonic seasonality and weather factors.
    Returns 24h-168h multi-step forecast with 95% confidence bands and feature importances.
    """
    return forecast_engine.train_and_forecast(
        forecast_horizon_hours=horizon_hours,
        n_estimators=n_estimators
    )

@router.get("/climate-correlation")
def get_climate_correlations():
    """
    Calculates Pearson correlation matrix and temperature sensitivity for marginal costs.
    """
    return climate_engine.compute_climate_correlations()

@router.get("/regulatory-corpus")
def get_regulatory_corpus(
    query: Optional[str] = Query(None, description="Search term in laws and articles"),
    category: Optional[str] = Query("ALL", description="Filter by category (ALMACENAMIENTO_BESS, PMGD_DISTRIBUCION, etc.)")
):
    """
    Search and retrieve Chilean energy regulations (DFL 4, Ley Almacenamiento 21.505, DS 88 PMGD, CNE Resoluciones).
    """
    return RegulatoryCorpusEngine.search_documents(query=query or "", category=category)

@router.get("/cen-api-check")
def check_cen_api():
    """
    Checks the status of the Coordinador Eléctrico Nacional v4 marginal cost API client.
    """
    return cen_client.fetch_marginal_costs_by_date("2026-08-01", "2026-08-22")
