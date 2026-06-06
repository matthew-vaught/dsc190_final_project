"""Build and format complete surf condition reports."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from surf_conditions import coops, ndbc, nws, sea_temperature
from surf_conditions.http import SurfConditionsError
from surf_conditions.locations import Location
from surf_conditions.models import Reading, SurfReport, Tide

PACIFIC = ZoneInfo("America/Los_Angeles")


def build_report(location: Location, now: datetime | None = None) -> SurfReport:
    generated_at = now or datetime.now(PACIFIC)

    predictions = coops.fetch_tide_predictions(location.coops_station, generated_at)
    pattern = coops.describe_tide_pattern(predictions, generated_at)
    try:
        tide_point = coops.fetch_latest_water_level(location.coops_station)
        tide_source = "NOAA CO-OPS observed water level"
    except SurfConditionsError:
        tide_point = coops.closest_prediction(predictions, generated_at)
        tide_source = "NOAA CO-OPS tide prediction"

    water_temperature = _fetch_water_temperature(location)

    return SurfReport(
        location=location,
        generated_at=generated_at,
        tide=Tide(
            height_ft=tide_point.value,
            pattern=pattern,
            observed_at=tide_point.timestamp,
            source=tide_source,
        ),
        weather=nws.fetch_current_weather(location.latitude, location.longitude),
        water_temperature=water_temperature,
    )


def format_report(report: SurfReport) -> str:
    return "\n".join(
        [
            f"{report.location.label} surf check: {report.location.beach}",
            f"Updated: {_format_time(report.generated_at)}",
            "",
            f"Tide: {report.tide.height_ft:.2f} ft MLLW, {report.tide.pattern}",
            f"Wind: {report.weather.wind}",
            f"Air temp: {report.weather.temperature_f} F",
            f"Cloudiness: {report.weather.cloudiness}",
            f"Water temp: {_format_water_temperature(report.water_temperature)}",
        ],
    )


def format_log_entry(report: SurfReport) -> str:
    return "\n".join(
        [
            "=" * 64,
            f"Area queried: {report.location.code}",
            f"Beach: {report.location.beach}",
            f"Queried at: {_format_time(report.generated_at)}",
            "",
            f"Tide: {report.tide.height_ft:.2f} ft MLLW, {report.tide.pattern}",
            f"Wind: {report.weather.wind}",
            f"Air temp: {report.weather.temperature_f} F",
            f"Cloudiness: {report.weather.cloudiness}",
            f"Water temp: {_format_water_temperature(report.water_temperature)}",
            "",
            "Sources:",
            f"- Tide: {report.tide.source}, {_format_time(report.tide.observed_at)}",
            f"- Weather: {report.weather.source}, {_format_time(report.weather.observed_at)}",
            _format_water_temperature_source(report.water_temperature),
            "",
        ],
    )


def _fetch_water_temperature(location: Location) -> Reading | None:
    try:
        point = coops.fetch_latest_water_temperature(location.coops_station)
        return Reading(
            value=f"{point.value:.1f} F",
            observed_at=point.timestamp,
            source="NOAA CO-OPS water temperature",
        )
    except SurfConditionsError:
        pass

    if not location.ndbc_station:
        return _fetch_sea_temperature_page(location)

    try:
        reading = ndbc.fetch_water_temperature(location.ndbc_station)
    except SurfConditionsError:
        return _fetch_sea_temperature_page(location)
    return Reading(
        value=f"{reading.water_temperature_f:.1f} F",
        observed_at=reading.observed_at,
        source=f"NOAA NDBC {location.ndbc_station}",
    )


def _fetch_sea_temperature_page(location: Location) -> Reading | None:
    if not location.sea_temperature_url:
        return None

    try:
        reading = sea_temperature.fetch_sea_surface_temperature(
            location.sea_temperature_url,
        )
    except SurfConditionsError:
        return None

    return Reading(
        value=f"{reading.temperature_f:.1f} F",
        observed_at=None,
        source=f"SeaTemperature.org NOAA/satellite SST for {reading.observed_on}",
    )


def _format_time(value: datetime | None) -> str:
    if value is None:
        return "time unavailable"
    return value.astimezone(PACIFIC).strftime("%Y-%m-%d %I:%M %p %Z")


def _format_water_temperature(reading: Reading | None) -> str:
    if reading is None:
        return "unavailable right now"
    return reading.value


def _format_water_temperature_source(reading: Reading | None) -> str:
    if reading is None:
        return "- Water temp: unavailable"
    return f"- Water temp: {reading.source}, {_format_time(reading.observed_at)}"
