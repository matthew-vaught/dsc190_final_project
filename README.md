# Surf Conditions CLI

A small command-line surf check for San Diego and Orange County. It pulls live or current online conditions for the beach you choose and reports the tide, tide direction, wind, air temperature, cloudiness, and water temperature in one terminal-friendly summary. This solves a very practical problem for me personally because now if I am ever working on my computer and I am thinking about going surfing soon, this provides me all of the information that I need to know to determine if I would want to go or not. The only two places I would really ever be surfing is San Diego when I am in school or Orange County over the summer, however I can always add more options later on to this tool if I branch out and start surfing in new places as well.

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
Wind: 10 mph SW
Air temp: 66 F
Cloudiness: Mostly Cloudy
Water temp: 66.2 F

Logged to: /home/vaugh/surf_conditions_log.txt
```

The CLI uses NOAA CO-OPS for tide data, the National Weather Service hourly
forecast for wind/weather, and NOAA CO-OPS or NDBC for water temperature when
available. If a local NOAA water-temperature sensor is unavailable, it falls
back to a current sea-surface temperature page that publishes NOAA/satellite
SST observations.

Each run also appends a neatly formatted entry to:

```text
~/surf_conditions_log.txt
```

The terminal output stays short, while the log file keeps the queried area,
timestamp, conditions, and data sources for each check.

To install from GitHub for grading or reuse:

```bash
uv add "git+https://github.com/<your-username>/<your-repo>.git"
surf-conditions sd
```
