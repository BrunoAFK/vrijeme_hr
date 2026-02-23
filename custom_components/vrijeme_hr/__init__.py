"""The Vrijeme HR integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_INTEGRATION_TYPE, DEFAULT_UPDATE_INTERVAL
from .coordinator import VrijemeHrvatskaDataUpdateCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Vrijeme HR from a config entry."""
    config = {**entry.data, **entry.options}
    integration_type = config.get(CONF_INTEGRATION_TYPE, "sensor")
    update_interval = int(
        config.get("update_interval", entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL))
    )

    coordinator = VrijemeHrvatskaDataUpdateCoordinator(
        hass=hass,
        city=entry.data["city"],
        update_interval=update_interval
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(f"Initial update failed: {err}") from err

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
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, hass.data[DOMAIN][entry.entry_id]["platforms"]
    ):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
