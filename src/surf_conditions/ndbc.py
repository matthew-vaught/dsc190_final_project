"""NOAA NDBC text-feed parsing for fallback water temperature."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from surf_conditions.http import SurfConditionsError, fetch_text

NDBC_URL = "https://www.ndbc.noaa.gov/data/realtime2/{station}.txt"
UTC = ZoneInfo("UTC")


@dataclass(frozen=True)
class NdbcReading:
    observed_at: datetime
    water_temperature_f: float


def fetch_water_temperature(station: str) -> NdbcReading:
    body = fetch_text(NDBC_URL.format(station=station.upper()))
    return parse_water_temperature(body)


def parse_water_temperature(body: str) -> NdbcReading:
    lines = [line.split() for line in body.splitlines() if line.strip()]
    if len(lines) < 3:
        raise SurfConditionsError("NDBC returned no recent observations")

    header = [column.lstrip("#") for column in lines[0]]
    try:
        wtmp_index = header.index("WTMP")
    except ValueError as error:
        raise SurfConditionsError(
            "NDBC feed does not include water temperature"
        ) from error

    for row in lines[2:]:
        if len(row) <= wtmp_index or row[wtmp_index] in {"MM", "-"}:
            continue
        observed_at = datetime(
            int(row[0]),
            int(row[1]),
            int(row[2]),
            int(row[3]),
            int(row[4]),
            tzinfo=UTC,
        )
        celsius = float(row[wtmp_index])
        return NdbcReading(
            observed_at=observed_at,
            water_temperature_f=(celsius * 9 / 5) + 32,
        )

    raise SurfConditionsError("NDBC feed has no usable water temperature reading")
