"""Conformance tests for the Canadian Forest Fire Weather Index System.

The first test is the one that matters: it reproduces the worked example published with
the standard itself, so anyone can check this implementation against the reference
without trusting us or installing anything beyond numpy and pandas.
"""

import pandas as pd

from infernis_fire.fwi import FWIService


def test_matches_van_wagner_pickett_worked_example():
    """Van Wagner & Pickett (1985), Forestry Technical Report 33.

    Standard season-startup state (FFMC 85, DMC 6, DC 15) advanced one April day at
    17.0 C, 42% RH, 25 km/h wind, no rain.
    """
    result = FWIService().compute_daily(
        temp=17.0, rh=42.0, wind=25.0, precip=0.0, month=4,
        prev_ffmc=85.0, prev_dmc=6.0, prev_dc=15.0,
    )

    assert result["ffmc"] == 87.7
    assert result["dmc"] == 8.5
    assert result["dc"] == 19.0
    assert result["isi"] == 10.9
    assert result["bui"] == 8.5
    assert result["fwi"] == 10.1


def test_rain_lowers_the_fine_fuel_code():
    """FFMC responds to rain within the day; the slower codes lag behind it."""
    dry = FWIService().compute_daily(
        temp=20.0, rh=35.0, wind=15.0, precip=0.0, month=7,
        prev_ffmc=90.0, prev_dmc=30.0, prev_dc=200.0,
    )
    wet = FWIService().compute_daily(
        temp=20.0, rh=35.0, wind=15.0, precip=5.0, month=7,
        prev_ffmc=90.0, prev_dmc=30.0, prev_dc=200.0,
    )

    assert wet["ffmc"] < dry["ffmc"]
    assert wet["dmc"] < dry["dmc"]
    assert wet["fwi"] < dry["fwi"]


def test_codes_stay_within_their_physical_ranges():
    """FFMC is bounded at 101 by construction; the cumulative codes never go negative."""
    for temp, rh, wind, precip in [
        (35.0, 5.0, 60.0, 0.0),     # extreme drying
        (-5.0, 100.0, 0.0, 50.0),   # extreme wetting
        (0.0, 50.0, 10.0, 0.0),
    ]:
        result = FWIService().compute_daily(
            temp=temp, rh=rh, wind=wind, precip=precip, month=6,
        )
        assert 0.0 <= result["ffmc"] <= 101.0
        assert result["dmc"] >= 0.0
        assert result["dc"] >= 0.0
        assert result["isi"] >= 0.0
        assert result["bui"] >= 0.0
        assert result["fwi"] >= 0.0


def test_season_carries_state_forward_day_to_day():
    """The codes are cumulative: a dry run must not reset between days."""
    weather = pd.DataFrame(
        {
            "temp": [20.0] * 5,
            "rh": [30.0] * 5,
            "wind": [15.0] * 5,
            "precip": [0.0] * 5,
            "month": [7] * 5,
        }
    )

    season = FWIService().compute_season(weather)

    assert len(season) == 5
    assert season["dc"].is_monotonic_increasing
    assert season["dmc"].is_monotonic_increasing
    assert season["dc"].iloc[-1] > season["dc"].iloc[0]
