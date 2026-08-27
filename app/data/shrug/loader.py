from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd


class ShrugLoadError(ValueError):
    pass


def _validate(frame: pd.DataFrame, required_columns: set[str]) -> pd.DataFrame:
    missing = required_columns - set(frame.columns)
    if missing:
        raise ShrugLoadError(f"Missing required columns: {sorted(missing)}")
    if "shrid2" in frame.columns and frame["shrid2"].duplicated().any():
        raise ShrugLoadError("shrid2 must be unique in a SHRID-level table")
    return frame


def load_table(path: str | Path, required_columns: set[str]) -> pd.DataFrame:
    """Load normalized SHRUG tables from CSV, Parquet, or Stata (.dta)."""
    source = Path(path)
    suffix = source.suffix.lower()
    if suffix == ".csv":
        frame = pd.read_csv(source)
    elif suffix in {".parquet", ".pq"}:
        frame = pd.read_parquet(source)
    elif suffix == ".dta":
        frame = pd.read_stata(source, convert_categoricals=False)
    else:
        raise ShrugLoadError(
            f"Unsupported SHRUG table format: {source.suffix}. "
            "Expected .dta, .csv, or .parquet."
        )
    return _validate(frame, required_columns)


def load_geodata(path: str | Path, required_columns: set[str] | None = None) -> gpd.GeoDataFrame:
    """Load verified SHRUG polygon data from GeoPackage or Shapefile."""
    source = Path(path)
    if source.suffix.lower() not in {".gpkg", ".shp"}:
        raise ShrugLoadError("Spatial SHRUG input must be .gpkg or .shp")
    frame = gpd.read_file(source)
    if required_columns:
        _validate(frame, required_columns)
    if frame.geometry.isna().any():
        raise ShrugLoadError("Spatial input contains null geometries")
    return frame
