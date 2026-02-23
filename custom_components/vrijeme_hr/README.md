# Vrijeme.hr Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

This integration provides **current weather data** from meteo.hr (Croatian Meteorological and Hydrological Service - DHMZ) for Home Assistant. **Please note that this integration does not retrieve forecast data, only current conditions are provided.** The XML feed is updated approximately once per hour.

## Features
- Weather sensor data for Croatian cities
- Available as both sensor entities and a basic weather entity
- Configurable update interval
- Multiple sensor options

## Recommended Usage
This integration is most effective when used for its sensor entities, which provide current weather measurements. While a weather entity is available, it only shows the current conditions and does not include forecast data.

### Recommended Frontend Cards
To make the most of this integration's sensor data, consider using the [Weather Chart Card](https://github.com/mlamberts78/weather-chart-card) custom card.

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
   - Select desired sensors (if "both" option is selected)

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
For bugs or feature requests, please create an issue in the GitHub repository.

## Data Source & Attribution
This integration uses official XML weather data feeds provided by DHMZ. The XML feed is available at [vrijeme.hr](https://vrijeme.hr/hrvatska_n.xml) while the official data provider site is [meteo.hr](https://meteo.hr/). The XML data is updated approximately once per hour.

The data usage is permitted by DHMZ with proper attribution. Visit [DHMZ XML Data Services](https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici) for more information about their data services.

## License
This integration is licensed under the Apache License 2.0.

### Data License
The weather data is provided by DHMZ (Croatian Meteorological and Hydrological Service) under the Open License - The Republic of Croatia. The data usage is permitted with the following conditions:
- The source (DHMZ) must be properly attributed
- Any modifications must be clearly stated
- The data can be used for both commercial and non-commercial purposes
- The data can be integrated into other applications and services

This integration complies with all DHMZ's data usage requirements and properly attributes all data to DHMZ as the source.

## Credits
- All weather data is provided by DHMZ (Croatian Meteorological and Hydrological Service)
- Integration developed by @BrunoAFK