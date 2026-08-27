from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Evidence(Generic[T]):
    """A value plus provenance required by ARTHA SETU."""

    value: T
    source: str
    vintage: str
    confidence_low: T | None = None
    confidence_high: T | None = None
    method: str | None = None

    @property
    def confidence_interval(self) -> tuple[T, T] | None:
        if self.confidence_low is None or self.confidence_high is None:
            return None
        return self.confidence_low, self.confidence_high
