"""NOAA CO-OPS tide and water-temperature access."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from surf_conditions.http import JsonObject, SurfConditionsError, fetch_json

COOPS_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
PACIFIC = ZoneInfo("America/Los_Angeles")


@dataclass(frozen=True)
class CoopsPoint:
    timestamp: datetime
    value: float


def fetch_latest_water_level(station: str) -> CoopsPoint:
    data = _fetch_coops_product(
        station,
        "water_level",
        {"date": "latest", "datum": "MLLW"},
    )
    return _first_point(data)


def fetch_latest_water_temperature(station: str) -> CoopsPoint:
    data = _fetch_coops_product(station, "water_temperature", {"date": "latest"})
    return _first_point(data)


def fetch_tide_predictions(station: str, now: datetime) -> list[CoopsPoint]:
    local_now = now.astimezone(PACIFIC)
    data = _fetch_coops_product(
        station,
        "predictions",
        {
            "begin_date": local_now.strftime("%Y%m%d"),
            "end_date": local_now.strftime("%Y%m%d"),
            "datum": "MLLW",
            "interval": "6",
        },
    )
    raw_predictions = data.get("predictions")
    if not isinstance(raw_predictions, list):
        raise SurfConditionsError("NOAA CO-OPS returned no tide predictions")
    return [_parse_point(item) for item in raw_predictions if isinstance(item, dict)]


def describe_tide_pattern(points: list[CoopsPoint], now: datetime) -> str:
    if len(points) < 2:
        return "unknown"

    local_now = now.astimezone(PACIFIC)
    before = max(
        (point for point in points if point.timestamp <= local_now),
        key=lambda point: point.timestamp,
        default=points[0],
    )
    after = min(
        (point for point in points if point.timestamp >= local_now),
        key=lambda point: point.timestamp,
        default=points[-1],
    )

    if after.value > before.value:
        return "going up"
    if after.value < before.value:
        return "receding"
    return "steady"


def closest_prediction(points: list[CoopsPoint], now: datetime) -> CoopsPoint:
    if not points:
        raise SurfConditionsError("NOAA CO-OPS returned no usable tide predictions")
    local_now = now.astimezone(PACIFIC)
    return min(points, key=lambda point: abs(point.timestamp - local_now))


def _fetch_coops_product(
    station: str,
    product: str,
    extra_params: dict[str, str],
) -> JsonObject:
    params = {
        "station": station,
        "product": product,
        "units": "english",
        "time_zone": "lst_ldt",
        "format": "json",
        "application": "surf_conditions",
    }
    params.update(extra_params)
    data = fetch_json(COOPS_URL, params)
    error = data.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        if isinstance(message, str):
            raise SurfConditionsError(message)
    return data


def _first_point(data: JsonObject) -> CoopsPoint:
    raw_points = data.get("data")
    if not isinstance(raw_points, list) or not raw_points:
        raise SurfConditionsError("NOAA CO-OPS returned no observation data")
    first = raw_points[0]
    if not isinstance(first, dict):
        raise SurfConditionsError("NOAA CO-OPS returned malformed observation data")
    return _parse_point(first)


def _parse_point(raw: dict[object, object]) -> CoopsPoint:
    raw_time = raw.get("t")
    raw_value = raw.get("v")
    if not isinstance(raw_time, str) or not isinstance(raw_value, str):
        raise SurfConditionsError("NOAA CO-OPS point is missing time or value")
    return CoopsPoint(
        timestamp=datetime.strptime(raw_time, "%Y-%m-%d %H:%M").replace(
            tzinfo=PACIFIC,
        ),
        value=float(raw_value),
    )
