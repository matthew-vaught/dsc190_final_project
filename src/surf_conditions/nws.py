"""National Weather Service hourly forecast access."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from surf_conditions.http import SurfConditionsError, fetch_json
from surf_conditions.models import Weather

POINTS_URL = "https://api.weather.gov/points/{latitude:.4f},{longitude:.4f}"


def fetch_current_weather(latitude: float, longitude: float) -> Weather:
    point_data = fetch_json(POINTS_URL.format(latitude=latitude, longitude=longitude))
    forecast_url = _string_property(point_data, "forecastHourly")
    forecast_data = fetch_json(forecast_url)
    periods = _properties(forecast_data).get("periods")
    if not isinstance(periods, list) or not periods:
        raise SurfConditionsError("NWS returned no hourly forecast periods")
    first = periods[0]
    if not isinstance(first, dict):
        raise SurfConditionsError("NWS returned a malformed hourly forecast")

    return Weather(
        temperature_f=_int_value(first, "temperature"),
        wind=f"{_string_value(first, 'windSpeed')} {_string_value(first, 'windDirection')}",
        cloudiness=_string_value(first, "shortForecast"),
        observed_at=_parse_nws_time(_string_value(first, "startTime")),
        source="NWS hourly forecast",
    )


def _string_property(data: dict[str, Any], key: str) -> str:
    value = _properties(data).get(key)
    if not isinstance(value, str):
        raise SurfConditionsError(f"NWS response is missing {key}")
    return value


def _properties(data: dict[str, Any]) -> dict[str, Any]:
    properties = data.get("properties")
    if not isinstance(properties, dict):
        raise SurfConditionsError("NWS response is missing properties")
    return properties


def _string_value(data: dict[object, object], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str):
        raise SurfConditionsError(f"NWS forecast is missing {key}")
    return value


def _int_value(data: dict[object, object], key: str) -> int:
    value = data.get(key)
    if not isinstance(value, int):
        raise SurfConditionsError(f"NWS forecast is missing {key}")
    return value


def _parse_nws_time(value: str) -> datetime:
    return datetime.fromisoformat(value)
