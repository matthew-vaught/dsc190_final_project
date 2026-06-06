"""Fallback sea-surface temperature page parsing."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from typing import Any, cast

from surf_conditions.http import SurfConditionsError, fetch_text

JSON_LD_RE = re.compile(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
    re.DOTALL,
)


@dataclass(frozen=True)
class SeaTemperatureReading:
    observed_on: date
    temperature_f: float


def fetch_sea_surface_temperature(url: str) -> SeaTemperatureReading:
    body = fetch_text(url)
    return parse_sea_surface_temperature(body)


def parse_sea_surface_temperature(body: str) -> SeaTemperatureReading:
    for match in JSON_LD_RE.finditer(body):
        try:
            payload = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if _string_value(payload, "@type") != "Observation":
            continue
        if _string_value(payload, "measuredProperty") != "Sea surface temperature":
            continue

        value = _object_value(payload, "value").get("value")
        observed_on = _string_value(payload, "observationDate")
        if observed_on is None:
            raise SurfConditionsError("Sea-temperature observation has no date")
        if not isinstance(value, int | float):
            raise SurfConditionsError("Sea-temperature observation has no value")
        celsius = float(value)
        return SeaTemperatureReading(
            observed_on=date.fromisoformat(observed_on),
            temperature_f=(celsius * 9 / 5) + 32,
        )

    raise SurfConditionsError("Could not find sea-temperature observation")


def _string_value(data: Any, key: str) -> str | None:
    if not isinstance(data, dict):
        return None
    value = data.get(key)
    if not isinstance(value, str):
        return None
    return value


def _object_value(data: Any, key: str) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise SurfConditionsError("Sea-temperature observation is malformed")
    value = data.get(key)
    if not isinstance(value, dict):
        raise SurfConditionsError("Sea-temperature observation is malformed")
    return cast(dict[str, Any], value)
