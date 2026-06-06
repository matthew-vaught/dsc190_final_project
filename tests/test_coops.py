from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from surf_conditions.coops import CoopsPoint, closest_prediction, describe_tide_pattern

PACIFIC = ZoneInfo("America/Los_Angeles")


def test_describe_tide_pattern_going_up() -> None:
    now = datetime(2026, 6, 6, 10, 3, tzinfo=PACIFIC)
    points = [
        CoopsPoint(datetime(2026, 6, 6, 10, 0, tzinfo=PACIFIC), 1.2),
        CoopsPoint(datetime(2026, 6, 6, 10, 6, tzinfo=PACIFIC), 1.3),
    ]

    assert describe_tide_pattern(points, now) == "going up"


def test_describe_tide_pattern_receding() -> None:
    now = datetime(2026, 6, 6, 10, 3, tzinfo=PACIFIC)
    points = [
        CoopsPoint(datetime(2026, 6, 6, 10, 0, tzinfo=PACIFIC), 2.0),
        CoopsPoint(datetime(2026, 6, 6, 10, 6, tzinfo=PACIFIC), 1.9),
    ]

    assert describe_tide_pattern(points, now) == "receding"


def test_closest_prediction_uses_nearest_timestamp() -> None:
    now = datetime(2026, 6, 6, 10, 5, tzinfo=PACIFIC)
    nearest = CoopsPoint(datetime(2026, 6, 6, 10, 6, tzinfo=PACIFIC), 3.4)
    points = [
        CoopsPoint(datetime(2026, 6, 6, 10, 0, tzinfo=PACIFIC), 3.2),
        nearest,
    ]

    assert closest_prediction(points, now) == nearest
