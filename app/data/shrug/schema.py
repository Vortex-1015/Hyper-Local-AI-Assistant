from __future__ import annotations

# Minimal required columns for the first Module 1 vertical slice.
# These names follow the SHRUG v2.2 metadata; adapters can map source-specific
# formats into this normalized contract.

PCA_REQUIRED = {
    "shrid2",
    "pc11_pca_tot_p",
    "pc11_pca_no_hh",
    "pc11_pca_tot_work_p",
    "pc11_pca_main_hh_p",
}

ECONOMIC_CENSUS_REQUIRED = {
    "shrid2",
    "ec13_emp_all",
    "ec13_emp_manuf",
    "ec13_emp_services",
}

SPATIAL_REQUIRED = {
    "shrid2",
    "latitude",
    "longitude",
}


def missing_columns(columns: set[str], required: set[str]) -> set[str]:
    return required - columns
