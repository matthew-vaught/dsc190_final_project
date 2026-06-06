"""Data models for surf reports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from surf_conditions.locations import Location


@dataclass(frozen=True)
class Reading:
    value: str
    observed_at: datetime | None
    source: str


@dataclass(frozen=True)
class Tide:
    height_ft: float
    pattern: str
    observed_at: datetime | None
    source: str


@dataclass(frozen=True)
class Weather:
    temperature_f: int
    wind: str
    cloudiness: str
    observed_at: datetime | None
    source: str


@dataclass(frozen=True)
class SurfReport:
    location: Location
    generated_at: datetime
    tide: Tide
    weather: Weather
    water_temperature: Reading | None
