from typing import Dict, List, Any
import numpy as np
import pandas as pd
from packages.costo_marginal.ml_forecast_engine import MLForecastEngine

class ClimateAnalyticsEngine:
    """
    Analyzes correlations and elasticities between meteorological variables
    (Temperature, Wind, Humidity, Rain) and electrical Marginal Costs in Chile.
    """

    def __init__(self, data_path: str = None):
        self.forecast_engine = MLForecastEngine(data_path=data_path)

    def compute_climate_correlations(self) -> Dict[str, Any]:
        df = self.forecast_engine.load_data()
        
        target_cols = [
            'costo_marginal', 'temperatura_c', 'velocidad_viento_ms',
            'humedad_porcentaje', 'presion_hpa', 'lluvia_mm'
        ]
        available_cols = [c for c in target_cols if c in df.columns]
        
        corr_matrix = df[available_cols].corr().round(3).to_dict()

        # Temperature elasticity ($/MWh per 1°C deviation above 25°C or below 8°C)
        cold_days = df[df['temperatura_c'] <= 8.0]['costo_marginal'].mean() if 'temperatura_c' in df.columns else 45.0
        mild_days = df[(df['temperatura_c'] > 8.0) & (df['temperatura_c'] < 25.0)]['costo_marginal'].mean() if 'temperatura_c' in df.columns else 35.0
        hot_days = df[df['temperatura_c'] >= 25.0]['costo_marginal'].mean() if 'temperatura_c' in df.columns else 48.0

        # Hourly seasonal profile (Hour 0 to 23 mean cost & temperature)
        hourly_profile = df.groupby('hora').agg({
            'costo_marginal': 'mean',
            'temperatura_c': 'mean' if 'temperatura_c' in df.columns else 'count'
        }).round(2).reset_index().to_dict(orient='records')

        return {
            "correlation_matrix": corr_matrix,
            "temperature_sensitivity": {
                "cold_spell_avg_cost_usd": round(float(cold_days), 2),
                "mild_weather_avg_cost_usd": round(float(mild_days), 2),
                "heatwave_avg_cost_usd": round(float(hot_days), 2),
                "heatwave_premium_pct": round(float(((hot_days - mild_days) / mild_days) * 100), 1) if mild_days > 0 else 0.0
            },
            "hourly_profile": hourly_profile
        }
