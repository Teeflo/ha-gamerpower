"""The GamerPower integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import (
    CONF_PLATFORMS,
    CONF_SCAN_INTERVAL,
    CONF_TYPES,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    VERSION,
)
from .coordinator import GamerPowerCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the GamerPower component."""
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.info("Initializing GamerPower integration version %s", VERSION)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up GamerPower from a config entry."""
    # Get configuration with options override
    platforms = entry.options.get(
        CONF_PLATFORMS, entry.data.get(CONF_PLATFORMS, [])
    )
    giveaway_types = entry.options.get(
        CONF_TYPES, entry.data.get(CONF_TYPES, [])
    )
    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    )

    # Create coordinator
    coordinator = GamerPowerCoordinator(
        hass,
        platforms=platforms,
        giveaway_types=giveaway_types,
        update_interval=scan_interval,
    )

    # Fetch initial data
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error("Error setting up GamerPower: %s", err)
        raise ConfigEntryNotReady from err

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener for options
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    # Register services
    await async_setup_services(hass, coordinator)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup_services(
    hass: HomeAssistant, coordinator: GamerPowerCoordinator
) -> None:
    """Set up services for GamerPower."""

    async def handle_refresh(call: ServiceCall) -> None:
        """Handle the refresh service call."""
        _LOGGER.info("Manually refreshing GamerPower data")
        await coordinator.async_request_refresh()

    async def handle_get_giveaway(call: ServiceCall) -> dict:
        """Handle getting a specific giveaway."""
        giveaway_id = call.data.get("giveaway_id")
        if giveaway_id:
            result = await coordinator.async_get_giveaway_details(giveaway_id)
            if result:
                return result
        return {}

    # Register services if not already registered
    if not hass.services.has_service(DOMAIN, "refresh"):
        hass.services.async_register(
            DOMAIN,
            "refresh",
            handle_refresh,
            schema=vol.Schema({}),
        )

    if not hass.services.has_service(DOMAIN, "get_giveaway"):
        hass.services.async_register(
            DOMAIN,
            "get_giveaway",
            handle_get_giveaway,
            schema=vol.Schema(
                {
                    vol.Required("giveaway_id"): cv.positive_int,
                }
            ),
        )
