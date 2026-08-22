import pandas as pd
import numpy as np
from typing import Optional

def calculate_yoy(series: pd.Series, periods: int = 252) -> pd.Series:
    """Calculate Year-over-Year percentage change: ((P_t - P_{t-N}) / P_{t-N}) * 100."""
    return ((series - series.shift(periods)) / series.shift(periods).abs()) * 100.0

def calculate_mom(series: pd.Series, periods: int = 21) -> pd.Series:
    """Calculate Month-over-Month percentage change."""
    return ((series - series.shift(periods)) / series.shift(periods).abs()) * 100.0

def calculate_rolling_ma(series: pd.Series, window: int = 20) -> pd.Series:
    """Calculate Rolling Simple Moving Average."""
    return series.rolling(window=window, min_periods=max(1, window // 3)).mean()

def calculate_rolling_z_score(series: pd.Series, window: int = 252) -> pd.Series:
    """Calculate Rolling Z-Score: (X_t - rolling_mean) / rolling_std."""
    mean = series.rolling(window=window, min_periods=max(2, window // 4)).mean()
    std = series.rolling(window=window, min_periods=max(2, window // 4)).std()
    # Avoid zero division
    std = std.replace(0, np.nan)
    return (series - mean) / std

def calculate_drawdown(series: pd.Series) -> pd.Series:
    """Calculate percentage drawdown from peak."""
    rolling_max = series.cummax()
    return ((series - rolling_max) / rolling_max.abs()) * 100.0

def calculate_realized_volatility(series: pd.Series, window: int = 21) -> pd.Series:
    """Calculate annualized rolling volatility on percentage returns."""
    pct_returns = series.pct_change()
    return pct_returns.rolling(window=window, min_periods=5).std() * np.sqrt(252) * 100.0
