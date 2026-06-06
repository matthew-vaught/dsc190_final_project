"""Command-line interface for surf condition checks."""

from __future__ import annotations

import argparse

from surf_conditions.locations import LOCATIONS


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
    print(f"{location.label} conditions are not wired up yet.")
    return 0
