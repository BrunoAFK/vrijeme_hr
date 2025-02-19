"""Config flow for Vrijeme.hr integration."""
from typing import Any, Dict, Optional
import voluptuous as vol
import aiohttp
import xmltodict
import logging
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_CITY,
    CONF_COUNTRY,
    CONF_UPDATE_INTERVAL,
    CONF_INTEGRATION_TYPE,
    CONF_SENSOR_OPTIONS,
    DEFAULT_UPDATE_INTERVAL,
    CROATIA_URL,
    EUROPE_URL,
    SUPPORTED_COUNTRIES,
    INTEGRATION_TYPES,
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
        self._country: Optional[str] = None
        self._integration_type: Optional[str] = None
        self._city: Optional[str] = None
        self._update_interval: Optional[int] = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VrijemeOptionsFlow(config_entry)

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._integration_type = user_input[CONF_INTEGRATION_TYPE]
            
            self._cities = await get_available_cities()
            
            if not self._cities:
                errors["base"] = "no_cities"
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({
                        vol.Required(CONF_INTEGRATION_TYPE): vol.In(INTEGRATION_TYPES)
                    }),
                    errors=errors
                )

            return await self.async_step_city()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_INTEGRATION_TYPE): vol.In(INTEGRATION_TYPES)
            }),
            errors=errors
        )

    async def async_step_city(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the city selection and sensor selection in one step."""
        errors = {}

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
            vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
        }
        
        # Add sensor selection if integration type is "both"
        if self._integration_type == "both":
            schema[vol.Required(CONF_SENSOR_OPTIONS)] = cv.multi_select(AVAILABLE_SENSORS)

        return self.async_show_form(
            step_id="city",
            data_schema=vol.Schema(schema)
        )

class VrijemeOptionsFlow(config_entries.OptionsFlow):
    """Handle Vrijeme options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
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
                ): int,
            })
        )