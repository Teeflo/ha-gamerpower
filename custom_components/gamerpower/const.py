"""Constants for the GamerPower integration."""
from datetime import timedelta
from typing import Final

DOMAIN: Final = "gamerpower"
VERSION: Final = "1.0.0"

# API Configuration
API_BASE_URL: Final = "https://www.gamerpower.com/api"
API_ENDPOINT_GIVEAWAYS: Final = "/giveaways"
API_ENDPOINT_GIVEAWAY: Final = "/giveaway"
API_ENDPOINT_FILTER: Final = "/filter"
API_ENDPOINT_WORTH: Final = "/worth"

# Default update interval (in minutes)
DEFAULT_SCAN_INTERVAL: Final = 30
MIN_SCAN_INTERVAL: Final = 5
MAX_SCAN_INTERVAL: Final = 1440  # 24 hours

# Configuration keys
CONF_PLATFORMS: Final = "platforms"
CONF_TYPES: Final = "types"
CONF_SCAN_INTERVAL: Final = "scan_interval"

# Available platforms
PLATFORMS: Final = {
    "pc": "PC",
    "steam": "Steam",
    "epic-games-store": "Epic Games Store",
    "ubisoft": "Ubisoft",
    "gog": "GOG",
    "itchio": "itch.io",
    "ps4": "PlayStation 4",
    "ps5": "PlayStation 5",
    "xbox-one": "Xbox One",
    "xbox-series-xs": "Xbox Series X|S",
    "switch": "Nintendo Switch",
    "android": "Android",
    "ios": "iOS",
    "vr": "VR",
    "battlenet": "Battle.net",
    "origin": "Origin",
    "drm-free": "DRM-Free",
}

# Available giveaway types
GIVEAWAY_TYPES: Final = {
    "game": "Full Game",
    "loot": "In-Game Loot",
    "beta": "Beta Access",
}

# Sensor types
SENSOR_TYPE_TOTAL_GIVEAWAYS: Final = "total_giveaways"
SENSOR_TYPE_TOTAL_WORTH: Final = "total_worth"
SENSOR_TYPE_LATEST_GIVEAWAY: Final = "latest_giveaway"

# Attribution
ATTRIBUTION: Final = "Data provided by GamerPower.com"
