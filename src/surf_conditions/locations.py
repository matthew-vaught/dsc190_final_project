"""Location definitions for supported surf spots."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    code: str
    label: str
    beach: str
    latitude: float
    longitude: float
    coops_station: str


LOCATIONS: dict[str, Location] = {
    "sd": Location(
        code="sd",
        label="San Diego",
        beach="Scripps Beach",
        latitude=32.8669,
        longitude=-117.2571,
        coops_station="9410230",
    ),
    "oc": Location(
        code="oc",
        label="Orange County",
        beach="Newport Beach",
        latitude=33.5934,
        longitude=-117.8827,
        coops_station="9410580",
    ),
}
