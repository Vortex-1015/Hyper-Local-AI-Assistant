from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


class ShrugLoadError(ValueError):
    pass


def load_table(path: str | Path, required_columns: set[str]) -> pd.DataFrame:
    """Load a development table and validate the minimal normalized contract.

    Supported first-pass formats are CSV and Parquet. Stata/GeoPackage adapters
    will be added once the official SHRUG v2.2 artifacts are staged locally.
    """
    source = Path(path)
    if source.suffix.lower() == ".csv":
        frame = pd.read_csv(source)
    elif source.suffix.lower() in {".parquet", ".pq"}:
        frame = pd.read_parquet(source)
    else:
        raise ShrugLoadError(
            f"Unsupported development format: {source.suffix}. "
            "Use CSV/Parquet until the verified v2.2 adapter is added."
        )

    missing = required_columns - set(frame.columns)
    if missing:
        raise ShrugLoadError(f"Missing required columns: {sorted(missing)}")
    return frame
