# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-29

### Added

- Initial release
- Support for tracking free games and giveaways from GamerPower API
- Platform filtering (Steam, Epic Games, PlayStation, Xbox, Nintendo Switch, and more)
- Type filtering (Full Games, In-Game Loot, Beta Access)
- Four sensors:
  - Total Giveaways count
  - Total Worth estimation
  - Latest Giveaway details
  - Active Giveaways List with platform grouping
- Manual refresh service (`gamerpower.refresh`)
- Get giveaway details service (`gamerpower.get_giveaway`)
- Configurable update interval (5-1440 minutes)
- New giveaway detection for automations
- Full French translation support
- Config flow UI for easy setup
- Options flow for updating preferences

### Technical

- Async implementation using aiohttp
- DataUpdateCoordinator for efficient data caching
- Full type hints throughout codebase
- HACS compatible structure
