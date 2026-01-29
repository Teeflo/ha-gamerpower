"""Sensor platform for GamerPower integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import GamerPowerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up GamerPower sensors from a config entry."""
    coordinator: GamerPowerCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = [
        GamerPowerTotalGiveawaysSensor(coordinator, entry),
        GamerPowerTotalWorthSensor(coordinator, entry),
        GamerPowerLatestGiveawaySensor(coordinator, entry),
        GamerPowerActiveGiveawaysListSensor(coordinator, entry),
    ]

    async_add_entities(entities)


class GamerPowerBaseSensor(CoordinatorEntity[GamerPowerCoordinator], SensorEntity):
    """Base class for GamerPower sensors."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: GamerPowerCoordinator,
        entry: ConfigEntry,
        sensor_type: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_name = name
        self._entry = entry

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="GamerPower Giveaways",
            manufacturer="GamerPower.com",
            model="Game Giveaway Tracker",
            configuration_url="https://www.gamerpower.com",
        )


class GamerPowerTotalGiveawaysSensor(GamerPowerBaseSensor):
    """Sensor showing total number of active giveaways."""

    _attr_icon = "mdi:gift"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, coordinator: GamerPowerCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, "total_giveaways", "Total Giveaways")

    @property
    def native_value(self) -> int:
        """Return the total number of giveaways."""
        if self.coordinator.data and "giveaways" in self.coordinator.data:
            return len(self.coordinator.data["giveaways"])
        return 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        attrs: dict[str, Any] = {}
        if self.coordinator.data:
            worth = self.coordinator.data.get("worth", {})
            attrs["active_giveaways_count"] = worth.get("active_giveaways_number", 0)
            
            # Count by type
            giveaways = self.coordinator.data.get("giveaways", [])
            type_counts: dict[str, int] = {}
            for giveaway in giveaways:
                gtype = giveaway.get("type", "unknown")
                type_counts[gtype] = type_counts.get(gtype, 0) + 1
            attrs["by_type"] = type_counts
        return attrs


class GamerPowerTotalWorthSensor(GamerPowerBaseSensor):
    """Sensor showing total worth of active giveaways."""

    _attr_icon = "mdi:currency-usd"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "USD"
    _attr_device_class = SensorDeviceClass.MONETARY

    def __init__(
        self, coordinator: GamerPowerCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, "total_worth", "Total Worth")

    @property
    def native_value(self) -> float | None:
        """Return the total worth."""
        if self.coordinator.data:
            worth = self.coordinator.data.get("worth", {})
            worth_str = worth.get("worth_estimation_usd", "0")
            # Parse worth string like "$1,234.56"
            if isinstance(worth_str, str):
                try:
                    return float(worth_str.replace("$", "").replace(",", "").replace("~", ""))
                except ValueError:
                    return None
            return worth_str
        return None


class GamerPowerLatestGiveawaySensor(GamerPowerBaseSensor):
    """Sensor showing the latest giveaway."""

    _attr_icon = "mdi:new-box"

    def __init__(
        self, coordinator: GamerPowerCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, "latest_giveaway", "Latest Giveaway")

    @property
    def native_value(self) -> str | None:
        """Return the title of the latest giveaway."""
        if self.coordinator.data:
            giveaways = self.coordinator.data.get("giveaways", [])
            if giveaways:
                return giveaways[0].get("title", "Unknown")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes about the latest giveaway."""
        attrs: dict[str, Any] = {}
        if self.coordinator.data:
            giveaways = self.coordinator.data.get("giveaways", [])
            if giveaways:
                latest = giveaways[0]
                attrs["id"] = latest.get("id")
                attrs["title"] = latest.get("title")
                attrs["type"] = latest.get("type")
                attrs["platforms"] = latest.get("platforms")
                attrs["worth"] = latest.get("worth")
                attrs["thumbnail"] = latest.get("thumbnail")
                attrs["image"] = latest.get("image")
                attrs["description"] = latest.get("description")
                attrs["instructions"] = latest.get("instructions")
                attrs["open_giveaway_url"] = latest.get("open_giveaway_url")
                attrs["gamerpower_url"] = latest.get("gamerpower_url")
                attrs["published_date"] = latest.get("published_date")
                attrs["end_date"] = latest.get("end_date")
                attrs["status"] = latest.get("status")
        return attrs


class GamerPowerActiveGiveawaysListSensor(GamerPowerBaseSensor):
    """Sensor with a list of all active giveaways in attributes."""

    _attr_icon = "mdi:format-list-bulleted"

    def __init__(
        self, coordinator: GamerPowerCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator, entry, "active_giveaways_list", "Active Giveaways List"
        )

    @property
    def native_value(self) -> int:
        """Return the count of active giveaways."""
        if self.coordinator.data:
            return len(self.coordinator.data.get("giveaways", []))
        return 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return all giveaways as attributes."""
        attrs: dict[str, Any] = {"giveaways": []}
        if self.coordinator.data:
            giveaways = self.coordinator.data.get("giveaways", [])
            # Store simplified giveaway info
            attrs["giveaways"] = [
                {
                    "id": g.get("id"),
                    "title": g.get("title"),
                    "type": g.get("type"),
                    "platforms": g.get("platforms"),
                    "worth": g.get("worth"),
                    "thumbnail": g.get("thumbnail"),
                    "open_giveaway_url": g.get("open_giveaway_url"),
                    "end_date": g.get("end_date"),
                }
                for g in giveaways[:50]  # Limit to 50 to avoid too large attributes
            ]
            
            # Group by platform
            by_platform: dict[str, list[str]] = {}
            for g in giveaways:
                platforms = g.get("platforms", "").split(", ")
                for platform in platforms:
                    if platform:
                        if platform not in by_platform:
                            by_platform[platform] = []
                        by_platform[platform].append(g.get("title", "Unknown"))
            attrs["by_platform"] = by_platform
            
            # New giveaways since last update
            new_giveaways = self.coordinator.data.get("new_giveaways", [])
            attrs["new_since_last_update"] = [
                g.get("title") for g in new_giveaways
            ]
        return attrs
