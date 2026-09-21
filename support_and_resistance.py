
# support and resistance.
from scipy.signal import find_peaks
import pandas as pd
import numpy as np

data = "link necessary data"

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


# clustering nearby swings
def cluster_levels(levels, tolerance=0.01):

    levels = sorted(levels)
    clusters = []

    for level in levels:

        if not clusters:
            clusters.append([level])
            continue

        cluster_mean = np.mean(clusters[-1])
        distance_from_cluster = abs(level - cluster_mean) / cluster_mean

        if distance_from_cluster <= tolerance:
            clusters[-1].append(level)
        else:
            clusters.append([level])

    return [
        {
            "level": np.mean(cluster),
            "touches": len(cluster)
        }
        for cluster in clusters
    ]



# finding highs and lows indices


def main():

    # dinding high and low indices
    high_indices, low_indices = find_swing_points(

    data = data,
    distance = 10,
    prominence = 1.0

    )

    # swing highs and swing lows
    swing_highs = data["High"].iloc[high_indices]
    swing_lows = data["Low"].iloc[low_indices]

    # resistance zones
    resistance_zones = cluster_levels(
        swing_highs.tolist(),
        tolerance = 0.01
    )

    # support zones
    support_zones = cluster_levels(
        swing_lows.tolist(),
        tolerance = 0.01
    )

    # filtering to meaningful zones:  a level has to be encountered twice
    resistance_zones = [
    zone for zone in resistance_zones
    if zone["touches"] >= 2
    ]

    support_zones = [
        zone for zone in support_zones
        if zone["touches"] >= 2
    ]


if __name__ == "__main__":
    main()