"""Data update coordinator for GamerPower."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_BASE_URL,
    API_ENDPOINT_FILTER,
    API_ENDPOINT_GIVEAWAYS,
    API_ENDPOINT_WORTH,
    ATTRIBUTION,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class GamerPowerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch data from GamerPower API."""

    def __init__(
        self,
        hass: HomeAssistant,
        platforms: list[str],
        giveaway_types: list[str],
        update_interval: int,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )
        self.platforms = platforms
        self.giveaway_types = giveaway_types
        self.session = async_get_clientsession(hass)
        self._last_giveaway_ids: set[int] = set()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from GamerPower API."""
        try:
            data: dict[str, Any] = {
                "giveaways": [],
                "worth": {},
                "new_giveaways": [],
                "attribution": ATTRIBUTION,
            }

            # Fetch giveaways
            giveaways = await self._fetch_giveaways()
            data["giveaways"] = giveaways

            # Detect new giveaways
            current_ids = {g["id"] for g in giveaways}
            if self._last_giveaway_ids:
                new_ids = current_ids - self._last_giveaway_ids
                data["new_giveaways"] = [
                    g for g in giveaways if g["id"] in new_ids
                ]
            self._last_giveaway_ids = current_ids

            # Fetch worth estimation
            worth = await self._fetch_worth()
            data["worth"] = worth

            return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with GamerPower API: {err}") from err
        except TimeoutError as err:
            raise UpdateFailed(f"Timeout fetching GamerPower data: {err}") from err

    async def _fetch_giveaways(self) -> list[dict[str, Any]]:
        """Fetch giveaways from API."""
        if self.platforms or self.giveaway_types:
            # Use filter endpoint for specific platforms/types
            url = f"{API_BASE_URL}{API_ENDPOINT_FILTER}"
            params = {}
            
            if self.platforms:
                params["platform"] = ".".join(self.platforms)
            if self.giveaway_types:
                params["type"] = ".".join(self.giveaway_types)
            
            async with self.session.get(
                url, params=params, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 201:
                    # No giveaways available
                    return []
                if response.status == 200:
                    return await response.json()
                _LOGGER.warning(
                    "Unexpected status %s from GamerPower API", response.status
                )
                return []
        else:
            # Fetch all giveaways
            url = f"{API_BASE_URL}{API_ENDPOINT_GIVEAWAYS}"
            async with self.session.get(
                url, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 201:
                    return []
                if response.status == 200:
                    return await response.json()
                _LOGGER.warning(
                    "Unexpected status %s from GamerPower API", response.status
                )
                return []

    async def _fetch_worth(self) -> dict[str, Any]:
        """Fetch total worth estimation from API."""
        url = f"{API_BASE_URL}{API_ENDPOINT_WORTH}"
        params = {}
        
        if self.platforms:
            params["platform"] = self.platforms[0]  # API only accepts one platform
        if self.giveaway_types:
            params["type"] = self.giveaway_types[0]  # API only accepts one type

        try:
            async with self.session.get(
                url, params=params, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}
        except Exception as err:
            _LOGGER.debug("Could not fetch worth data: %s", err)
            return {}

    async def async_get_giveaway_details(self, giveaway_id: int) -> dict[str, Any] | None:
        """Fetch details for a specific giveaway."""
        url = f"{API_BASE_URL}/giveaway"
        params = {"id": giveaway_id}
        
        try:
            async with self.session.get(
                url, params=params, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception as err:
            _LOGGER.error("Error fetching giveaway %s: %s", giveaway_id, err)
            return None
