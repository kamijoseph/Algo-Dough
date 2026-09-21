
# support and resistance.
from scipy.signal import find_peaks
import pandas as pd

# 1. find swings
def find_swing_points(data: pd.DataFrame, distance:int, prominence=None):

    high_indices, _ = find_peaks(
        data["High"].values,
        distance = distance,
        prominence = prominence
    )

    low_indices, _ = find_peaks(
        -data["Low"].values,
        distance = distance,
        prominence = prominence
    )

    return high_indices, low_indices