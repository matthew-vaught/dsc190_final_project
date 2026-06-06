from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from surf_conditions.locations import LOCATIONS
from surf_conditions.logging import append_report_log
from surf_conditions.models import Reading, SurfReport, Tide, Weather

PACIFIC = ZoneInfo("America/Los_Angeles")


def test_append_report_log_writes_entry(tmp_path: Path) -> None:
    report = SurfReport(
        location=LOCATIONS["sd"],
        generated_at=datetime(2026, 6, 6, 9, 30, tzinfo=PACIFIC),
        tide=Tide(
            height_ft=2.42,
            pattern="going up",
            observed_at=None,
            source="NOAA CO-OPS observed water level",
        ),
        weather=Weather(
            temperature_f=68,
            wind="8 mph W",
            cloudiness="Partly Cloudy",
            observed_at=None,
            source="NWS hourly forecast",
        ),
        water_temperature=Reading(
            value="64.1 F",
            observed_at=None,
            source="NOAA CO-OPS water temperature",
        ),
    )
    log_path = tmp_path / "surf.txt"

    written_path = append_report_log(report, log_path)

    assert written_path == log_path
    content = log_path.read_text(encoding="utf-8")
    assert "Area queried: sd" in content
    assert "Water temp: 64.1 F" in content
    assert "Sources:" in content
