"""Config flow for GamerPower integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .const import (
    API_BASE_URL,
    API_ENDPOINT_GIVEAWAYS,
    CONF_PLATFORMS,
    CONF_SCAN_INTERVAL,
    CONF_TYPES,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    GIVEAWAY_TYPES,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)


class GamerPowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GamerPower."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate API connection
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(
                    f"{API_BASE_URL}{API_ENDPOINT_GIVEAWAYS}", timeout=10
                ) as response:
                    if response.status in (200, 201):
                        # Check if already configured
                        await self.async_set_unique_id(DOMAIN)
                        self._abort_if_unique_id_configured()

                        return self.async_create_entry(
                            title="GamerPower Giveaways",
                            data=user_input,
                        )
                    errors["base"] = "cannot_connect"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # Build form schema
        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_PLATFORMS, default=[]
                ): cv.multi_select(PLATFORMS),
                vol.Optional(
                    CONF_TYPES, default=[]
                ): cv.multi_select(GIVEAWAY_TYPES),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> GamerPowerOptionsFlowHandler:
        """Get the options flow handler."""
        return GamerPowerOptionsFlowHandler(config_entry)


class GamerPowerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for GamerPower."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current values
        current_platforms = self.config_entry.data.get(CONF_PLATFORMS, [])
        current_types = self.config_entry.data.get(CONF_TYPES, [])
        current_interval = self.config_entry.data.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        # Override with options if set
        current_platforms = self.config_entry.options.get(
            CONF_PLATFORMS, current_platforms
        )
        current_types = self.config_entry.options.get(CONF_TYPES, current_types)
        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, current_interval
        )

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_PLATFORMS, default=current_platforms
                ): cv.multi_select(PLATFORMS),
                vol.Optional(
                    CONF_TYPES, default=current_types
                ): cv.multi_select(GIVEAWAY_TYPES),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=current_interval
                ): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL),
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)
