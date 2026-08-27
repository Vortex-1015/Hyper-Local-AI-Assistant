from __future__ import annotations

from dataclasses import dataclass, field

from app.core.evidence import Evidence


@dataclass(frozen=True)
class MarketReach:
    """Computed catchment-market features; values must remain provenance-backed."""

    radius_km: int
    population: Evidence[int]
    households: Evidence[int]
    source_units: int


@dataclass(frozen=True)
class EconomicProfile:
    non_farm_employment: Evidence[int]
    manufacturing_employment: Evidence[int]
    services_employment: Evidence[int]


@dataclass(frozen=True)
class FeasibilitySeed:
    location_shrid2: str
    market_5km: MarketReach
    market_10km: MarketReach
    economic_profile: EconomicProfile
    warnings: list[str] = field(default_factory=list)
