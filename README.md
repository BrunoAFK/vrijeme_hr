# Vrijeme.hr Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

This integration provides weather data from Vrijeme.hr (Croatian Meteorological and Hydrological Service - DHMZ) for Home Assistant.

## Features
- Real-time weather data for Croatian cities
- Supports both sensor and weather entities
- Configurable update interval
- Multiple sensor options (temperature, humidity, pressure, wind, etc.)

## Installation

### HACS Installation
1. Open HACS
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Add"
7. Find "Vrijeme.hr Weather" in the integrations list
8. Click "Download"
9. Restart Home Assistant

### Manual Installation
1. Copy the `vrijeme_hr` folder from `custom_components` to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings -> Devices & Services
2. Click "Add Integration"
3. Search for "Vrijeme.hr Weather"
4. Follow the configuration steps:
   - Select integration type (sensors, weather, or both)
   - Select your city
   - Configure update interval
   - Select desired sensors (if "both" option selected)

## Available Sensors
- Temperature
- Humidity
- Pressure
- Pressure Tendency
- Wind Speed
- Wind Direction
- Weather Condition
- Latitude
- Longitude

## Supported Cities
All major Croatian cities with DHMZ weather stations are supported.

## Support
- For bugs/feature requests, please create an issue in the GitHub repository
- For questions, please use the Home Assistant community forum

## Data Source & Attribution
This integration uses official XML weather data feeds provided by DHMZ (Croatian Meteorological and Hydrological Service - https://meteo.hr/). The data is sourced from:
- Main data feed: https://vrijeme.hr/hrvatska_n.xml
- Data update frequency: Every hour

The data usage is permitted by DHMZ with proper attribution. Visit [DHMZ XML Data Services](https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici) for more information about their data services.

[Rest of README remains the same...]a Services](https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici).

For more information about available XML services, visit the [DHMZ XML Data Services page](https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici).

## License
MIT License

## Credits
- All weather data is provided by DHMZ (Croatian Meteorological and Hydrological Service)
- Integration developed by @BrunoAFK