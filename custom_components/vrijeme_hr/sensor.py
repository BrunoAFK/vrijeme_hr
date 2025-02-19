"""Support for Vrijeme.hr sensors."""
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
    CONF_SENSOR_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Vrijeme.hr sensor."""
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
                VrijemeSensor(
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
        _LOGGER.error("Error setting up Vrijeme.hr sensors: %s", err, exc_info=True)
        raise

class VrijemeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Vrijeme.hr sensor."""

    def __init__(self, coordinator, sensor_type, sensor_info, city):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._sensor_info = sensor_info
        self._city = city
        self._attr_unique_id = f"vrijeme_{city}_{sensor_type}"
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
            "name": f"Vrijeme.hr {city}",
            "manufacturer": "DHMZ",
            "model": "Weather Station",
            "configuration_url": "https://vrijeme.hr/",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            _LOGGER.warning("No data available for %s", self._attr_name)
            return None
            
        value = self.coordinator.data.get(self._sensor_type)
        
        # Return None if value is None
        if value is None:
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
            return direction_map.get(value, value)
            
        elif self._sensor_type == "pressure_tendency":
            return self._process_pressure_trend(value)
            
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