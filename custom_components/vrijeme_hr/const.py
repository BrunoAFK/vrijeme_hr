"""Constants for the Vrijeme HR integration."""
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
CONF_COUNTRY = "country"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_INTEGRATION_TYPE = "integration_type"
CONF_WEATHER_SENSORS = "weather_sensors"  # instead of sensor_options

DEFAULT_UPDATE_INTERVAL = 3600

CROATIA_URL = "https://vrijeme.hr/hrvatska_n.xml"
EUROPE_URL = "https://vrijeme.hr/europa_n.xml"

SUPPORTED_COUNTRIES = {
    "croatia": "Croatia (Hrvatska)"
}

INTEGRATION_TYPES = ["sensor", "weather", "both"]
CONF_SENSOR_OPTIONS = "sensor_options"

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
