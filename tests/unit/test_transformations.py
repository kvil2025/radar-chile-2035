import pandas as pd
import numpy as np
from packages.indicators.transformations import (
    calculate_yoy, calculate_mom, calculate_rolling_ma, 
    calculate_rolling_z_score, calculate_drawdown
)

def test_calculate_yoy_and_mom():
    data = [100.0, 105.0, 110.0, 120.0]
    s = pd.Series(data)
    
    mom = calculate_mom(s, periods=1)
    assert round(mom.iloc[1], 2) == 5.0
    assert round(mom.iloc[3], 2) == 9.09

def test_calculate_rolling_ma():
    data = [10.0, 20.0, 30.0, 40.0, 50.0]
    s = pd.Series(data)
    ma = calculate_rolling_ma(s, window=3)
    assert ma.iloc[2] == 20.0
    assert ma.iloc[4] == 40.0

def test_calculate_rolling_z_score():
    data = np.random.normal(loc=100.0, scale=10.0, size=50)
    s = pd.Series(data)
    z = calculate_rolling_z_score(s, window=20)
    assert len(z) == 50
    assert not z.dropna().empty

def test_calculate_drawdown():
    data = [100.0, 120.0, 110.0, 90.0, 130.0]
    s = pd.Series(data)
    dd = calculate_drawdown(s)
    assert dd.iloc[0] == 0.0
    assert dd.iloc[1] == 0.0
    assert round(dd.iloc[2], 2) == -8.33
    assert round(dd.iloc[3], 2) == -25.0
    assert dd.iloc[4] == 0.0
