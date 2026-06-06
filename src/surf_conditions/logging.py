"""Append surf reports to a local text log."""

from __future__ import annotations

from pathlib import Path

from surf_conditions.models import SurfReport
from surf_conditions.report import format_log_entry

DEFAULT_LOG_FILENAME = "surf_conditions_log.txt"


def default_log_path() -> Path:
    return Path.home() / DEFAULT_LOG_FILENAME


def append_report_log(report: SurfReport, path: Path | None = None) -> Path:
    log_path = path or default_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as file:
        file.write(format_log_entry(report))
    return log_path
