from __future__ import annotations

from datetime import date

from surf_conditions.sea_temperature import parse_sea_surface_temperature


def test_parse_sea_surface_temperature_json_ld() -> None:
    body = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Observation",
      "measuredProperty": "Sea surface temperature",
      "value": {"@type": "QuantitativeValue", "value": 18.1, "unitCode": "CEL"},
      "observationDate": "2026-06-06"
    }
    </script>
    """

    reading = parse_sea_surface_temperature(body)

    assert reading.observed_on == date(2026, 6, 6)
    assert reading.temperature_f == 64.58
