from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

import pandas as pd

from app.core.evidence import Evidence
from app.models.market import MarketReach

EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two WGS84 coordinates in kilometres."""
    lat1_r, lat2_r = radians(lat1), radians(lat2)
    dlat = lat2_r - lat1_r
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def calculate_market_reach(
    location_shrid2: str,
    latitude: float,
    longitude: float,
    population: pd.DataFrame,
    spatial: pd.DataFrame,
    radius_km: int,
    *,
    source: str = "SHRUG v2.2",
    vintage: str = "2011",
) -> MarketReach:
    """Aggregate population and households for source units within a radius.

    This first implementation uses point-to-point great-circle distance. The
    production version will use verified SHRUG polygons/PostGIS intersection.
    """
    required_pop = {"shrid2", "pc11_pca_tot_p", "pc11_pca_no_hh"}
    required_spatial = {"shrid2", "latitude", "longitude"}
    if missing := required_pop - set(population.columns):
        raise ValueError(f"Population data missing columns: {sorted(missing)}")
    if missing := required_spatial - set(spatial.columns):
        raise ValueError(f"Spatial data missing columns: {sorted(missing)}")

    joined = population.merge(spatial[list(required_spatial)], on="shrid2", how="inner")
    distances = joined.apply(
        lambda row: haversine_km(latitude, longitude, row["latitude"], row["longitude"]),
        axis=1,
    )
    selected = joined.loc[distances <= radius_km]

    pop = int(selected["pc11_pca_tot_p"].sum())
    households = int(selected["pc11_pca_no_hh"].sum())
    evidence_pop = Evidence(
        pop,
        source,
        vintage,
        method=f"Sum of source units within {radius_km} km of {location_shrid2}",
    )
    evidence_hh = Evidence(
        households,
        source,
        vintage,
        method=f"Sum of source units within {radius_km} km of {location_shrid2}",
    )
    return MarketReach(radius_km, evidence_pop, evidence_hh, len(selected))
