import pandas as pd

from app.features.module1.market_reach import calculate_market_reach


def test_market_reach_uses_radius_and_returns_evidence():
    population = pd.DataFrame(
        {
            "shrid2": ["TEST-001", "TEST-002", "TEST-003", "TEST-004"],
            "pc11_pca_tot_p": [1200, 850, 1600, 540],
            "pc11_pca_no_hh": [280, 190, 360, 125],
        }
    )
    spatial = pd.DataFrame(
        {
            "shrid2": ["TEST-001", "TEST-002", "TEST-003", "TEST-004"],
            "latitude": [13.0800, 13.1050, 13.1350, 13.1850],
            "longitude": [80.2700, 80.2950, 80.2450, 80.3500],
        }
    )

    result = calculate_market_reach(
        "TEST-001",
        13.0800,
        80.2700,
        population,
        spatial,
        10,
    )

    assert result.radius_km == 10
    assert result.source_units == 3
    assert result.population.value == 3650
    assert result.households.value == 830
    assert result.population.source == "SHRUG v2.2"
    assert result.population.vintage == "2011"


def test_market_reach_can_exclude_distant_unit():
    population = pd.DataFrame(
        {
            "shrid2": ["TEST-001", "TEST-004"],
            "pc11_pca_tot_p": [1200, 540],
            "pc11_pca_no_hh": [280, 125],
        }
    )
    spatial = pd.DataFrame(
        {
            "shrid2": ["TEST-001", "TEST-004"],
            "latitude": [13.0800, 13.1850],
            "longitude": [80.2700, 80.3500],
        }
    )

    result = calculate_market_reach(
        "TEST-001", 13.0800, 80.2700, population, spatial, 5
    )

    assert result.source_units == 1
    assert result.population.value == 1200
    assert result.households.value == 280
