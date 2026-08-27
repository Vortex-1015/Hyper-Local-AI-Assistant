# SHRUG v2.2 acquisition

ARTHA SETU uses SHRUG as a source dataset for the Module 1 hyper-local feasibility engine.

## Source of truth

Use the official Development Data Lab SHRUG v2.2 download portal:

- https://www.devdatalab.org/shrug_download/
- https://docs.devdatalab.org/

Do not mix SHRUG versions. v2.2 is the required baseline.

## Initial acquisition scope

Acquire these modules first:

1. Core Keys / SHRID2 geography
2. Open Polygons
3. Spatial Statistics
4. 2011 Population Census Abstract
5. 2011 Village Directory
6. 2013 Economic Census

RBI and current-market datasets are later layers and are not required for the first Market Reach vertical slice.

## Local layout

Place downloaded source files under:

`data/raw/shrug/v2.2/`

The raw directory is intentionally excluded from source control except for its `.gitkeep` marker. Raw SHRUG data must not be committed to this repository.

## Acquisition principles

- Preserve the original downloaded files unchanged.
- Record SHRUG version, source URL, retrieval timestamp and file checksum.
- Validate expected columns before transformation.
- Normalize useful tables to Parquet for application use.
- Keep source vintage attached to every derived numerical feature through ARTHA SETU's Evidence contract.

## Important limitation

The official SHRUG portal uses an interactive download mechanism. This repository therefore does not hard-code guessed download URLs. The acquisition implementation should be filled in only after the actual v2.2 download endpoints/files have been verified.
