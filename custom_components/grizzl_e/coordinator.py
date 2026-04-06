"""Data coordinator for Grizzl-E EV Charger."""
import logging
from datetime import timedelta

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class GrizzlECoordinator(DataUpdateCoordinator):
    """Grizzl-E data coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize coordinator."""
        # Get scan interval from options (if changed) or data (initial setup)
        scan_interval = entry.options.get(
            CONF_SCAN_INTERVAL,
            entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.host = entry.data[CONF_HOST]
        self.session = async_get_clientsession(hass)
        self.entry = entry

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with self.session.post(
                f"http://{self.host}/main",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error communicating with API: {response.status}")
                return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
