"""Weather platform for Vrijeme.hr integration."""
from homeassistant.components.weather import WeatherEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, get_weather_condition  # Import the function here

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Vrijeme.hr weather platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([VrijemeWeather(coordinator, entry.data)])

class VrijemeWeather(WeatherEntity):
    """Implementation of Vrijeme.hr weather platform."""

    def init(self, coordinator, config):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._config = config
        self._attr_unique_id = f"vrijemeweather{config['city']}"
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
    def native_temperature(self):
        """Return the current temperature."""
        return self.coordinator.data.get("temperature")

    @property
    def native_pressure(self):
        """Return the current pressure."""
        return self.coordinator.data.get("pressure")

    @property
    def humidity(self):
        """Return the current humidity."""
        return self.coordinator.data.get("humidity")

    @property
    def native_wind_speed(self):
        """Return the current wind speed."""
        return self.coordinator.data.get("wind_speed")

    @property
    def wind_bearing(self):
        """Return the current wind bearing."""
        return self.coordinator.data.get("wind_direction")

    @property
    def condition(self):
        """Return current condition."""
        vrijeme = self.coordinator.data.get("vrijeme", "")
        return get_weather_condition(vrijeme)