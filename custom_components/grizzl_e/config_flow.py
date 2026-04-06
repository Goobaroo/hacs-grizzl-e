"""Config flow for Grizzl-E EV Charger integration."""
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_SCAN_INTERVAL, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=10, max=300)
        ),
    }
)


class GrizzlEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Grizzl-E EV Charger."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            # Test connection
            session = async_get_clientsession(self.hass)
            try:
                async with session.post(
                    f"http://{host}/main", timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Use serial number as unique ID if available
                        unique_id = data.get("serialNum", host)

                        await self.async_set_unique_id(unique_id)
                        self._abort_if_unique_id_configured()

                        return self.async_create_entry(
                            title=data.get("model", DEFAULT_NAME),
                            data={
                                CONF_HOST: host,
                                CONF_SCAN_INTERVAL: user_input.get(
                                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                                ),
                            },
                        )
                    else:
                        errors["base"] = "cannot_connect"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception as err:
                _LOGGER.exception("Unexpected exception: %s", err)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return GrizzlEOptionsFlow(config_entry)


class GrizzlEOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Grizzl-E."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.data.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                }
            ),
        )
