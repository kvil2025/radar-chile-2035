import math
import numpy as np

def normalize_min_max(value: float, min_val: float, max_val: float, direction: int = 1) -> float:
    """
    Normalizes a numeric observation into a bounded 0-100 score.
    direction = +1: Higher raw value yields higher score (e.g. Copper price for Chile Opportunity).
    direction = -1: Higher raw value yields lower score / higher stress.
    """
    if max_val == min_val:
        return 50.0

    # Clip to bounds
    clipped = max(min_val, min(max_val, value))
    scaled = ((clipped - min_val) / (max_val - min_val)) * 100.0

    if direction == -1:
        return round(100.0 - scaled, 2)
    return round(scaled, 2)

def normalize_z_score_sigmoid(value: float, mean: float, std: float, direction: int = 1) -> float:
    """
    Normalizes a value using standardized Z-score mapped through logistic sigmoid to 0-100.
    50 represents historical neutral mean.
    """
    if std <= 0 or math.isnan(std):
        return 50.0

    z = (value - mean) / std
    if direction == -1:
        z = -z

    # Sigmoid function centered at 0 with smooth scale
    sigmoid = 1.0 / (1.0 + math.exp(-z * 0.8))
    return round(sigmoid * 100.0, 2)
