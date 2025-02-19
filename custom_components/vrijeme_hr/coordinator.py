from datetime import timedelta
import logging
import aiohttp
import xmltodict
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import CROATIA_URL, EUROPE_URL, WEATHER_MAPPING

_LOGGER = logging.getLogger(name)

class VrijemeDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Vrijeme.hr data."""

    def init(self, hass, city, update_interval):
        """Initialize."""
        self.city = city
        self.url = CROATIA_URL

        super().init(
            hass,
            _LOGGER,
            name=f"vrijemehr{city}",
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self):
        """Fetch data from Vrijeme.hr."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")

                    xml_data = await response.text()
                    data = xmltodict.parse(xml_data)

                    # Find the city data
                    city_data = None
                    for grad in data["Hrvatska"]["Grad"]:
                        if grad["GradIme"] == self.city:
                            city_data = grad
                            break

                    if city_data is None:
                        raise UpdateFailed(f"City {self.city} not found in data")

                    return {
                        "temperature": float(city_data["Podatci"]["Temp"]) if city_data["Podatci"]["Temp"] != "-" else None,
                        "humidity": int(city_data["Podatci"]["Vlaga"]) if city_data["Podatci"]["Vlaga"] != "-" else None,
                        "pressure": float(city_data["Podatci"]["Tlak"]) if city_data["Podatci"]["Tlak"] != "-" else None,
                        "pressure_tendency": float(city_data["Podatci"]["TlakTend"]) if city_data["Podatci"]["TlakTend"] != "-" else None,
                        "wind_speed": float(city_data["Podatci"]["VjetarBrzina"]) if city_data["Podatci"]["VjetarBrzina"] != "-" else None,
                        "wind_direction": city_data["Podatci"]["VjetarSmjer"] if city_data["Podatci"]["VjetarSmjer"] != "-" else None,
                        "vrijeme": city_data["Podatci"]["Vrijeme"].lower() if city_data["Podatci"]["Vrijeme"] != "-" else "",
                        "latitude": float(city_data["Lat"]) if "Lat" in city_data else None,
                        "longitude": float(city_data["Lon"]) if "Lon" in city_data else None
                    }

            except Exception as err:
                raise UpdateFailed(f"Error fetching data: {err}")