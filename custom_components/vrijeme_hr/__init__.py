"""The Vrijeme.hr integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_INTEGRATION_TYPE
from .coordinator import VrijemeDataUpdateCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Vrijeme.hr from a config entry."""
    integration_type = entry.data.get(CONF_INTEGRATION_TYPE, "sensor")

    coordinator = VrijemeDataUpdateCoordinator(
        hass=hass,
        city=entry.data["city"],
        update_interval=entry.data["update_interval"]
    )

    await coordinator.async_config_entry_first_refresh()

    platforms = []
    if integration_type in ["sensor", "both"]:
        platforms.append("sensor")
    if integration_type in ["weather", "both"]:
        platforms.append("weather")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "platforms": platforms
    }

    await hass.config_entries.async_forward_entry_setups(entry, platforms)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, hass.data[DOMAIN][entry.entry_id]["platforms"]
    ):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok