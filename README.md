# Vrijeme HR for Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

`vrijeme_hr` is an unofficial Home Assistant weather integration for Croatia that exposes current observations as sensors and/or a weather entity.

## What this integration does
- Fetches current weather measurements for a selected Croatian city
- Supports `sensor`, `weather`, or both
- Uses Home Assistant UI config flow
- Supports configurable update interval

## Important limitation
This integration provides **current observations only** (not multi-day forecast output).

## Data source
- Source: DHMZ (Croatian Meteorological and Hydrological Service)
- Data is fetched from public DHMZ XML feeds.

## Quick start
1. Install via HACS (Custom Repository) or copy manually to `custom_components/vrijeme_hr`.
2. Restart Home Assistant.
3. Add integration in Devices & Services.
4. Select city and preferred integration type.

## Installation
### HACS (recommended)
1. Open HACS.
2. Go to `Integrations`.
3. Open `Custom repositories`.
4. Add this repository as category `Integration`.
5. Install `Vrijeme HR`.
6. Restart Home Assistant.

### Manual
1. Copy `custom_components/vrijeme_hr` into your HA `custom_components` directory.
2. Restart Home Assistant.

## Configuration
`Settings -> Devices & Services -> Add Integration -> Vrijeme HR`

Choose:
- integration type (`sensor`, `weather`, `both`)
- city
- update interval

## Available sensor fields
- temperature
- humidity
- pressure
- pressure tendency
- wind speed
- wind direction
- weather condition
- latitude
- longitude

## Reliability notes
- Robust numeric parsing for XML values
- Better handling of missing/invalid data
- Options changes reload properly
- Duplicate city entries are prevented

## Troubleshooting
- If city list is empty: source feed may be temporarily unavailable.
- If entities are `unknown/unavailable`: wait for next poll and check HA logs.
- If values look stale: verify integration reload and network access.

## HACS updates
HACS shows updates when a newer release/tag exists and `manifest.json` version is higher.

Recommended release flow:
1. Bump `custom_components/vrijeme_hr/manifest.json` version.
2. Push to `main`.
3. Publish release/tag `vX.Y.Z`.

## Attribution
- Data source: DHMZ
- This is an unofficial community integration and not an official DHMZ product.

## Support
Please use GitHub Issues for bug reports and feature requests.
