"""Command-line interface for surf condition checks."""

from __future__ import annotations

import argparse

from surf_conditions.http import SurfConditionsError
from surf_conditions.locations import LOCATIONS
from surf_conditions.report import build_report, format_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="surf-conditions",
        description="Check live surf-relevant conditions for SD or OC.",
    )
    parser.add_argument(
        "location",
        choices=sorted(LOCATIONS),
        help="Use 'sd' for Scripps Beach or 'oc' for Newport Beach.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    location = LOCATIONS[args.location]
    try:
        report = build_report(location)
    except SurfConditionsError as error:
        parser.exit(1, f"surf-conditions: {error}\n")
    print(format_report(report))
    return 0
