from __future__ import annotations

import hashlib
import json
from pathlib import Path


EXPECTED_V2_2_FILES = {
    "population": "pc11_pca_clean_shrid.dta",
    "economic_census": "ec13_shrid.dta",
    "spatial_stats": "shrid2_spatial_stats.dta",
    "geography": "shrid2.gpkg",
}


def sha256(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def validate_staging(root: str | Path) -> dict[str, object]:
    root = Path(root)
    found = {}
    missing = []
    for key, filename in EXPECTED_V2_2_FILES.items():
        path = root / filename
        if path.exists():
            found[key] = {"path": str(path), "sha256": sha256(path)}
        else:
            missing.append({"key": key, "filename": filename})
    return {"root": str(root), "found": found, "missing": missing}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate_staging(args.root)
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(text + "\n")
    else:
        print(text)
