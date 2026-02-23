from datetime import timedelta
import logging
import re
import xmltodict
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import CROATIA_URL

_LOGGER = logging.getLogger(__name__)

class VrijemeDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Vrijeme.hr data."""

    def __init__(self, hass, city, update_interval):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"vrijeme_hr_{city}",
            update_interval=timedelta(seconds=update_interval),
        )
        
        self.city = city
        self.url = CROATIA_URL

    def _clean_num(self, value) -> str:
        """Normalize numeric string from XML (remove ANSI/control chars and symbols)."""
        if value is None:
            return ""
        text = str(value).strip()
        # Strip ANSI escape sequences and keep numeric-relevant characters only.
        text = re.sub(r"\x1B\[[0-9;?]*[ -/]*[@-~]", "", text)
        text = re.sub(r"[^0-9+\-.,]", "", text)
        # XML sometimes contains commas as decimal separators.
        return text.replace(",", ".")

    def _to_float(self, value):
        """Convert XML numeric value to float safely."""
        text = self._clean_num(value)
        if not text or text == "-":
            return None
        try:
            return float(text)
        except (TypeError, ValueError):
            return None

    def _to_int(self, value):
        """Convert XML numeric value to int safely."""
        parsed = self._to_float(value)
        if parsed is None:
            return None
        try:
            return int(round(parsed))
        except (TypeError, ValueError):
            return None

    async def _async_update_data(self):
        """Fetch data from Vrijeme.hr."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self.url, timeout=30) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error fetching data: {response.status}")

                xml_data = await response.text()
                data = xmltodict.parse(xml_data)

                # Find selected city in feed.
                city_data = None
                for grad in data["Hrvatska"]["Grad"]:
                    if grad["GradIme"] == self.city:
                        city_data = grad
                        break

                if city_data is None:
                    raise UpdateFailed(f"City {self.city} not found in data")

                pod = city_data.get("Podatci", {})
                previous = self.data if isinstance(self.data, dict) else {}
                wind_direction = str(pod.get("VjetarSmjer", "")).strip()
                if wind_direction in {"", "-"}:
                    wind_direction = None
                vrijeme_raw = str(pod.get("Vrijeme", "")).strip()
                pressure_tendency = self._to_float(pod.get("TlakTend"))
                if pressure_tendency is None:
                    pressure_tendency = previous.get("pressure_tendency")

                return {
                    "temperature": self._to_float(pod.get("Temp")),
                    "humidity": self._to_int(pod.get("Vlaga")),
                    "pressure": self._to_float(pod.get("Tlak")),
                    "pressure_tendency": pressure_tendency,
                    "wind_speed": self._to_float(pod.get("VjetarBrzina")),
                    "wind_direction": wind_direction,
                    "vrijeme": vrijeme_raw.lower() if vrijeme_raw not in {"", "-"} else "",
                    "latitude": self._to_float(city_data.get("Lat")),
                    "longitude": self._to_float(city_data.get("Lon")),
                }

        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
