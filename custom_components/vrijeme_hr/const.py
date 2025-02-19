"""Constants for the Vrijeme.hr integration."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTemperature,
    PERCENTAGE,
    UnitOfPressure,
    UnitOfSpeed,
)

DOMAIN = "vrijeme_hr"
CONF_CITY = "city"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_INTEGRATION_TYPE = "integration_type"
CONF_SENSOR_OPTIONS = "sensor_options"
CONF_ENABLE_FORECAST = "enable_forecast"
CONF_DEBUG_LOGGING = "enable_debug_logging"

FORECAST_DAYS = 7  # Since the XML provides 7 days of forecast
FORECAST_HOURS = 24  # Hours per day for hourly forecast

DEFAULT_UPDATE_INTERVAL = 3600

CROATIA_URL = "https://vrijeme.hr/hrvatska_n.xml"
FORECAST_URL = "https://prognoza.hr/sedam/hrvatska/7d_meteogrami.xml"

INTEGRATION_TYPES = {
    "sensor": "Sensors Only",
    "weather": "Weather Only", 
    "weather_forecast": "Weather with Forecast",
    "both": "Both Weather and Sensors",
    "both_forecast": "Both Weather, Sensors and Forecast"
}

AVAILABLE_SENSORS = {
    "temperature": "Temperature",
    "humidity": "Humidity",
    "pressure": "Pressure",
    "pressure_tendency": "Pressure Tendency",
    "wind_speed": "Wind Speed",
    "wind_direction": "Wind Direction",
    "condition": "Weather Condition",
    "latitude": "Latitude",
    "longitude": "Longitude"
}

SENSOR_TYPES = {
    "temperature": {
        "name": AVAILABLE_SENSORS["temperature"],
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "humidity": {
        "name": AVAILABLE_SENSORS["humidity"],
        "unit": PERCENTAGE,
        "icon": "mdi:water-percent",
        "device_class": SensorDeviceClass.HUMIDITY,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "pressure": {
        "name": AVAILABLE_SENSORS["pressure"],
        "unit": UnitOfPressure.HPA,
        "icon": "mdi:gauge",
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "pressure_tendency": {
        "name": AVAILABLE_SENSORS["pressure_tendency"],
        "unit": UnitOfPressure.HPA,
        "icon": "mdi:trending-up",
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "wind_speed": {
        "name": AVAILABLE_SENSORS["wind_speed"],
        "unit": UnitOfSpeed.KILOMETERS_PER_HOUR,
        "icon": "mdi:weather-windy",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "wind_direction": {
        "name": AVAILABLE_SENSORS["wind_direction"],
        "unit": "°",
        "icon": "mdi:compass",
        "device_class": None,
        "state_class": None,  
    },
    "condition": {
        "name": AVAILABLE_SENSORS["condition"],
        "unit": None,
        "icon": "mdi:weather-partly-cloudy",
        "device_class": None,
        "state_class": None,
    },
    "latitude": {
        "name": AVAILABLE_SENSORS["latitude"],
        "unit": "°",
        "icon": "mdi:latitude",
        "device_class": None,
        "state_class": None,
    },
    "longitude": {
        "name": AVAILABLE_SENSORS["longitude"],
        "unit": "°",
        "icon": "mdi:longitude",
        "device_class": None,
        "state_class": None,
    }
}

FORECAST_SENSORS = {
    "forecast_temperature": "Forecast Temperature",
    "forecast_humidity": "Forecast Humidity",
    "forecast_pressure": "Forecast Pressure",
    "forecast_wind_speed": "Forecast Wind Speed",
    "forecast_wind_direction": "Forecast Wind Direction",
    "forecast_condition": "Forecast Condition",
    "forecast_precipitation": "Forecast Precipitation"
}

FORECAST_SENSOR_TYPES = {
    "forecast_temperature": {
        "name": FORECAST_SENSORS["forecast_temperature"],
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "forecast_humidity": {
        "name": FORECAST_SENSORS["forecast_humidity"],
        "unit": PERCENTAGE,
        "icon": "mdi:water-percent",
        "device_class": SensorDeviceClass.HUMIDITY,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "forecast_pressure": {
        "name": FORECAST_SENSORS["forecast_pressure"],
        "unit": UnitOfPressure.HPA,
        "icon": "mdi:gauge",
        "device_class": SensorDeviceClass.PRESSURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "forecast_wind_speed": {
        "name": FORECAST_SENSORS["forecast_wind_speed"],
        "unit": UnitOfSpeed.KILOMETERS_PER_HOUR,
        "icon": "mdi:weather-windy",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "forecast_wind_direction": {
        "name": FORECAST_SENSORS["forecast_wind_direction"],
        "unit": "°",
        "icon": "mdi:compass",
        "device_class": None,
        "state_class": None,
    },
    "forecast_condition": {
        "name": FORECAST_SENSORS["forecast_condition"],
        "unit": None,
        "icon": "mdi:weather-partly-cloudy",
        "device_class": None,
        "state_class": None,
    },
    "forecast_precipitation": {
        "name": FORECAST_SENSORS["forecast_precipitation"],
        "unit": "mm",
        "icon": "mdi:water",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    }
}

ATTRIBUTION = "Data provided by DHMZ (Croatian Meteorological and Hydrological Service)"
MANUFACTURER = "DHMZ"

WEATHER_MAPPING = {
    # Clear & Sunny conditions
    "vedro": "clear-night",  # when it's clear at night
    "sunčano": "sunny",
    
    # Cloudy conditions
    "potpuno oblačno": "cloudy",
    "pretežno oblačno": "cloudy",
    
    # Partly cloudy conditions
    "pretežno vedro": "partlycloudy",
    "umjereno oblačno": "partlycloudy",
    
    # Foggy conditions
    "magla": "fog",
    "maglovito": "fog",
    
    # Rain conditions
    "slaba kiša": "rainy",
    "kiša": "rainy",
    "jaka kiša": "pouring",
    
    # Snow conditions
    "slab snijeg": "snowy",
    "snijeg": "snowy",
    
    # Lightning/Storm conditions
    "grmljavina": "lightning",
    "munja": "lightning",
    "grmljavina, kiša": "lightning-rainy",
    
    # Hail
    "tuča": "hail",
    
    # Wind conditions
    "povjetarac": "windy",
    "lahor": "windy",
    "jak vjetar": "windy",
    "vjetrovito": "windy",
    "slab vjetar": "windy",
    "umjeren vjetar": "windy",
    "umjereno jak vjetar": "windy",
}

def get_weather_condition(vrijeme: str) -> str:
    """Get the weather condition based on the vrijeme value."""
    # First check for exact matches
    if vrijeme in WEATHER_MAPPING:
        return WEATHER_MAPPING[vrijeme]
    
    # Check for combined conditions
    conditions = vrijeme.split(',')
    if len(conditions) > 1:
        # Check for wind + cloudy combinations
        wind_conditions = {"povjetarac", "lahor", "jak vjetar", "vjetrovito", "slab vjetar", "umjeren vjetar", "umjereno jak vjetar"}
        cloud_conditions = {"potpuno oblačno", "pretežno oblačno"}
        
        conditions = {cond.strip() for cond in conditions}
        if conditions & wind_conditions and conditions & cloud_conditions:
            return "windy-cloudy"
    
    # If no match found, return exceptional
    return "exceptional"