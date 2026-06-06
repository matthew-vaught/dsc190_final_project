from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from surf_conditions.locations import LOCATIONS
from surf_conditions.models import Reading, SurfReport, Tide, Weather
from surf_conditions.report import format_report

PACIFIC = ZoneInfo("America/Los_Angeles")


def test_format_report_includes_requested_conditions() -> None:
    timestamp = datetime(2026, 6, 6, 9, 30, tzinfo=PACIFIC)
    report = SurfReport(
        location=LOCATIONS["sd"],
        generated_at=timestamp,
        tide=Tide(
            height_ft=2.42,
            pattern="going up",
            observed_at=timestamp,
            source="NOAA CO-OPS observed water level",
        ),
        weather=Weather(
            temperature_f=68,
            wind="8 mph W",
            cloudiness="Partly Cloudy",
            observed_at=timestamp,
            source="NWS hourly forecast",
        ),
        water_temperature=Reading(
            value="64.1 F",
            observed_at=timestamp,
            source="NOAA CO-OPS water temperature",
        ),
    )

    output = format_report(report)

    assert "Tide: 2.42 ft MLLW, going up" in output
    assert "Wind: 8 mph W" in output
    assert "Air temp: 68 F" in output
    assert "Cloudiness: Partly Cloudy" in output
    assert "Water temp: 64.1 F" in output
