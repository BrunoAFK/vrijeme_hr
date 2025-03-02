"""Config flow for Vrijeme.hr integration."""
from typing import Any, Dict, Optional
import voluptuous as vol
import aiohttp
import xmltodict
import logging
import os
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_CITY,
    CONF_UPDATE_INTERVAL,
    CONF_INTEGRATION_TYPE,
    CONF_SENSOR_OPTIONS,
    DEFAULT_UPDATE_INTERVAL,
    CROATIA_URL,
    AVAILABLE_SENSORS,
)

_LOGGER = logging.getLogger(__name__)

async def get_available_cities() -> list[str]:
    """Get list of available cities from the XML."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CROATIA_URL) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to fetch data from %s: %s", CROATIA_URL, response.status)
                    return []
                xml_data = await response.text()
                data = xmltodict.parse(xml_data)
                
                cities = []
                for grad in data["Hrvatska"]["Grad"]:
                    cities.append(grad["GradIme"])
                
                _LOGGER.debug("Found %d cities for Croatia", len(cities))
                return sorted(cities)
    except Exception as err:
        _LOGGER.error("Error fetching cities: %s", err)
        return []

class VrijemeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vrijeme.hr."""

    VERSION = 1
    
    def __init__(self):
        """Initialize flow."""
        self._cities: list[str] = []
        self._integration_type: Optional[str] = None
        self._city: Optional[str] = None
        self._update_interval: Optional[int] = None
        self._is_croatian = None  # Will be determined at runtime

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VrijemeOptionsFlow(config_entry)

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        # Try to detect language from environment
        import os
        language_env = os.environ.get("LANGUAGE", "")
        lang_setting = os.environ.get("LANG", "")
        
        self._is_croatian = "hr" in language_env.lower() or "hr" in lang_setting.lower()
        _LOGGER.debug("Language detection from env: %s, %s => is_croatian = %s", 
                      language_env, lang_setting, self._is_croatian)

        # Use appropriate translation based on detected language
        if self._is_croatian:
            integration_options = {
                "sensor": "Samo senzori",
                "weather": "Samo vremenska prognoza",
                "both": "Prognoza i senzori"
            }
        else:
            integration_options = {
                "sensor": "Sensors Only",
                "weather": "Weather Only",
                "both": "Both Weather and Sensors"
            }

        if user_input is not None:
            self._integration_type = user_input[CONF_INTEGRATION_TYPE]
            
            self._cities = await get_available_cities()
            
            if not self._cities:
                errors["base"] = "no_cities"
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({
                        vol.Required(CONF_INTEGRATION_TYPE): vol.In(integration_options)
                    }),
                    errors=errors
                )

            return await self.async_step_city()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_INTEGRATION_TYPE): vol.In(integration_options)
            }),
            errors=errors
        )

    async def async_step_city(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the city selection and sensor selection in one step."""
        errors = {}

        # Select the appropriate sensor labels based on language
        if self._is_croatian:
            sensor_labels = {
                "temperature": "Temperatura",
                "humidity": "Vlažnost",
                "pressure": "Tlak zraka",
                "pressure_tendency": "Tendencija tlaka",
                "wind_speed": "Brzina vjetra",
                "wind_direction": "Smjer vjetra",
                "condition": "Vremenske prilike",
                "latitude": "Geografska širina",
                "longitude": "Geografska dužina"
            }
            update_interval_description = "Učestalost ažuriranja u sekundama (zadano: 3600)"
        else:
            sensor_labels = {
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
            update_interval_description = "Update interval in seconds (default: 3600)"

        if user_input is not None:
            data = {
                CONF_CITY: user_input[CONF_CITY],
                CONF_INTEGRATION_TYPE: self._integration_type,
                CONF_UPDATE_INTERVAL: user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
            }
            
            # If integration type is "both", include sensor options
            if self._integration_type == "both":
                data[CONF_SENSOR_OPTIONS] = user_input.get(CONF_SENSOR_OPTIONS, [])

            return self.async_create_entry(
                title=f"Vrijeme.hr {user_input[CONF_CITY]}",
                data=data
            )

        # Build schema based on integration type
        schema = {
            vol.Required(CONF_CITY): vol.In(self._cities),
            vol.Optional(
                CONF_UPDATE_INTERVAL, 
                default=DEFAULT_UPDATE_INTERVAL, 
                description=update_interval_description
            ): int,
        }
        
        # Add sensor selection if integration type is "both"
        if self._integration_type == "both":
            schema[vol.Required(CONF_SENSOR_OPTIONS)] = cv.multi_select(sensor_labels)

        return self.async_show_form(
            step_id="city",
            data_schema=vol.Schema(schema)
        )

class VrijemeOptionsFlow(config_entries.OptionsFlow):
    """Handle Vrijeme options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self._is_croatian = None

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        # Try to detect language using the same approach
        language_env = os.environ.get("LANGUAGE", "")
        lang_setting = os.environ.get("LANG", "")
        
        self._is_croatian = "hr" in language_env.lower() or "hr" in lang_setting.lower()
        _LOGGER.debug("Options flow - Language detection from env: %s, %s => is_croatian = %s", 
                      language_env, lang_setting, self._is_croatian)
        
        # Get appropriate description based on language
        update_interval_description = (
            "Učestalost ažuriranja u sekundama" 
            if self._is_croatian 
            else "Update interval in seconds"
        )

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                    ),
                    description=update_interval_description,
                ): int,
            })
        )