# Surf Conditions CLI

A small command-line surf check for San Diego and Orange County. It pulls live
or current online conditions for the beach you choose and reports the tide,
tide direction, wind, air temperature, cloudiness, and water temperature in one
terminal-friendly summary.

## Usage

Run the tool with either `sd` for Scripps Beach or `oc` for Newport Beach:

```bash
uv run surf-conditions sd
```

```bash
uv run surf-conditions oc
```

Example output:

```text
San Diego surf check: Scripps Beach
Updated: 2026-06-06 01:56 PM PDT

Tide: 3.65 ft MLLW, going up
Tide source: NOAA CO-OPS observed water level, 2026-06-06 01:48 PM PDT
Wind: 10 mph SW
Air temp: 66 F
Cloudiness: Mostly Cloudy
Weather source: NWS hourly forecast, 2026-06-06 01:00 PM PDT
Water temp: 66.2 F (NOAA CO-OPS water temperature, 2026-06-06 01:48 PM PDT)
```

The CLI uses NOAA CO-OPS for tide data, the National Weather Service hourly
forecast for wind/weather, and NOAA CO-OPS or NDBC for water temperature when
available. If a local NOAA water-temperature sensor is unavailable, it falls
back to a current sea-surface temperature page that publishes NOAA/satellite
SST observations.

To install from GitHub for grading or reuse:

```bash
uv add "git+https://github.com/<your-username>/<your-repo>.git"
surf-conditions sd
```
