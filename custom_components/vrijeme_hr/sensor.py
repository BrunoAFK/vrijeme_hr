"""Support for Vrijeme HR sensors."""
import logging
from typing import Any, Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTemperature,
    PERCENTAGE,
    UnitOfPressure,
    UnitOfSpeed,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_TYPES,
    CONF_INTEGRATION_TYPE,
    CONF_SENSOR_OPTIONS,  # Changed from CONF_SENSORS to CONF_SENSOR_OPTIONS
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Vrijeme HR sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    try:
        # Determine which sensors to create based on integration type
        if entry.data[CONF_INTEGRATION_TYPE] == "both":
            # If "both", only create selected sensors
            selected_sensors = entry.data.get(CONF_SENSOR_OPTIONS, [])
            available_sensors = {k: v for k, v in SENSOR_TYPES.items() if k in selected_sensors}
        else:
            # If "sensor", create all sensors
            available_sensors = SENSOR_TYPES

        entities = []
        for sensor_type, sensor_info in available_sensors.items():
            entities.append(
                VrijemeHrvatskaSensor(
                    coordinator,
                    sensor_type,
                    sensor_info,
                    entry.data["city"]
                )
            )
        
        if entities:
            async_add_entities(entities)
            _LOGGER.info("Successfully set up %d sensors for %s", len(entities), entry.data["city"])
        else:
            _LOGGER.warning("No sensors to set up for %s based on configuration", entry.data["city"])
        
    except Exception as err:
        _LOGGER.error("Error setting up Vrijeme HR sensors: %s", err, exc_info=True)
        raise

class VrijemeHrvatskaSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Vrijeme HR sensor."""

    def __init__(self, coordinator, sensor_type, sensor_info, city):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._sensor_info = sensor_info
        self._city = city
        self._attr_unique_id = f"vrijeme_hr_{city}_{sensor_type}"
        self._attr_name = f"{city} {sensor_info['name']}"
        self._attr_native_unit_of_measurement = sensor_info["unit"]
        self._attr_device_class = sensor_info["device_class"]
        self._attr_state_class = sensor_info["state_class"]
        self._attr_icon = sensor_info["icon"]

        # Add attribution
        self._attr_attribution = "Data provided by DHMZ (Croatian Meteorological and Hydrological Service)"
        
        # Add device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, city)},
            "name": f"Vrijeme HR {city}",
            "manufacturer": "DHMZ",
            "model": "Weather Station",
            "configuration_url": "https://meteo.hr/",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            _LOGGER.debug("%s: Coordinator data is None", self._attr_name)
            return None
            
        # Special handling for condition sensor - look for "vrijeme" key instead and convert it
        if self._sensor_type == "condition":
            vrijeme = self.coordinator.data.get("vrijeme")
            if vrijeme is None or vrijeme == '-':
                return None
            from .const import get_weather_condition
            value = get_weather_condition(vrijeme)
        else:
            value = self.coordinator.data.get(self._sensor_type)
        
        _LOGGER.debug("%s: Raw value from coordinator: %s", self._attr_name, value)
        
        # Return None if value is None or '-'
        if value is None or value == '-':
            return None
            
        # Special handling for different sensor types
        if self._sensor_type == "wind_direction":
            # Return wind direction as degrees
            direction_map = {
                "N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5,
                "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
                "S": 180, "SSW": 202.5, "SW": 225, "WSW": 247.5,
                "W": 270, "WNW": 292.5, "NW": 315, "NNW": 337.5,
                "C": None  # Handle 'C' by returning None
            }
            converted_value = direction_map.get(value, None)
            _LOGGER.debug("%s: Converted wind direction from %s to %s", 
                        self._attr_name, value, converted_value)
            return converted_value
            
        elif self._sensor_type == "pressure_tendency":
            converted_value = self._process_pressure_trend(value)
            _LOGGER.debug("%s: Converted pressure tendency from %s to %s", 
                        self._attr_name, value, converted_value)
            return converted_value
        
        _LOGGER.debug("%s: Returning value: %s", self._attr_name, value)    
        return value

    def _process_pressure_trend(self, value: str) -> Optional[float]:
        """Process pressure trend value."""
        if value is None or value == "-" or value == "":
            return None
        try:
            trend = float(value)
            # Explicitly return 0.0 if the value is zero
            return 0.0 if trend == 0 else trend
        except (ValueError, TypeError):
            _LOGGER.warning("Invalid pressure trend value: %s", value)
            return None
