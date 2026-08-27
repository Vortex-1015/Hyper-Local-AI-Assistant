from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    """Resolved administrative/geographic identity for an entrepreneur location."""

    shrid2: str
    village_or_town: str
    subdistrict: str | None
    district: str | None
    state: str | None
    latitude: float | None = None
    longitude: float | None = None
