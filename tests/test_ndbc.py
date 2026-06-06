from __future__ import annotations

from surf_conditions.ndbc import parse_water_temperature


def test_parse_water_temperature_from_ndbc_feed() -> None:
    body = "\n".join(
        [
            "#YY MM DD hh mm WDIR WSPD GST WVHT DPD APD MWD PRES ATMP WTMP",
            "#yr mo dy hr mn degT m/s m/s m sec sec degT hPa degC degC",
            "2026 06 06 16 20 270 3.1 4.1 MM MM MM MM 1013.2 18.5 19.2",
        ],
    )

    reading = parse_water_temperature(body)

    assert reading.water_temperature_f == 66.56
