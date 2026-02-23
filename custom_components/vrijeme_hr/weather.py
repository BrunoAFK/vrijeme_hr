"""Weather platform for Vrijeme.hr integration."""
from homeassistant.components.weather import WeatherEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, get_weather_condition

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Vrijeme.hr weather platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([VrijemeWeather(coordinator, entry.data)])

class VrijemeWeather(CoordinatorEntity, WeatherEntity):
    """Implementation of Vrijeme.hr weather platform."""

    def __init__(self, coordinator, config):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config = config
        self._attr_unique_id = f"vrijeme_weather_{config['city']}"
        self._attr_name = f"Vrijeme.hr {config['city']}"
        
        # Add device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config['city'])},
            "name": f"Vrijeme.hr {config['city']}",
            "manufacturer": "DHMZ",
            "model": "Weather Station",
            "configuration_url": "https://vrijeme.hr/",
        }

    @property
    def condition(self):
        """Return current condition."""
        if not self.coordinator.data:
            return None
        vrijeme = self.coordinator.data.get("vrijeme", "")
        return get_weather_condition(vrijeme)

    @property
    def native_temperature(self):
        """Return the current temperature."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("temperature")

    @property
    def native_pressure(self):
        """Return the current pressure."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("pressure")

    @property
    def humidity(self):
        """Return the current humidity."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("humidity")

    @property
    def native_wind_speed(self):
        """Return the current wind speed."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("wind_speed")

    @property
    def wind_bearing(self):
        """Return the current wind bearing."""
        if not self.coordinator.data:
            return None
        value = self.coordinator.data.get("wind_direction")
        direction_map = {
            "N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5,
            "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
            "S": 180, "SSW": 202.5, "SW": 225, "WSW": 247.5,
            "W": 270, "WNW": 292.5, "NW": 315, "NNW": 337.5,
            "C": None
        }
        return direction_map.get(value, None)
