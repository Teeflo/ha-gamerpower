<p align="center">
  <img src="images/logo.png" alt="GamerPower Logo" height="150">
</p>

# GamerPower Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A custom Home Assistant integration that connects to the [GamerPower API](https://www.gamerpower.com/api) to automatically retrieve information about free games, game keys, and ongoing giveaways.

## Features

- **Track Free Games & Giveaways**: Automatically fetch active giveaways from GamerPower
- **Platform Filtering**: Filter by platform (Steam, Epic Games, PlayStation, Xbox, Nintendo Switch, etc.)
- **Type Filtering**: Filter by type (Full Games, In-Game Loot, Beta Access)
- **Worth Estimation**: See the total estimated value of active giveaways
- **New Giveaway Detection**: Get notified when new giveaways appear
- **Configurable Update Interval**: Set how often to check for updates (5-1440 minutes)

## Sensors

| Sensor | Description |
|--------|-------------|
| `sensor.gamerpower_total_giveaways` | Total number of active giveaways |
| `sensor.gamerpower_total_worth` | Total estimated value in USD |
| `sensor.gamerpower_latest_giveaway` | Latest giveaway with full details |
| `sensor.gamerpower_active_giveaways_list` | Complete list with platform grouping |

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL and select "Integration" as the category
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/gamerpower` folder
2. Copy it to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings > Devices & Services > Add Integration**
2. Search for "GamerPower Giveaways"
3. Configure your preferred platforms and giveaway types
4. Set your desired update interval

## Services

### `gamerpower.refresh`
Manually refresh giveaway data.

### `gamerpower.get_giveaway`
Get detailed information about a specific giveaway by ID.

```yaml
service: gamerpower.get_giveaway
data:
  giveaway_id: 525
```

## Automation Examples

### Notify on New Free Games

```yaml
automation:
  - alias: "New Free Game Alert"
    trigger:
      - platform: state
        entity_id: sensor.gamerpower_latest_giveaway
    condition:
      - condition: template
        value_template: "{{ trigger.from_state.state != trigger.to_state.state }}"
    action:
      - service: notify.mobile_app
        data:
          title: "New Free Game!"
          message: "{{ states('sensor.gamerpower_latest_giveaway') }}"
          data:
            url: "{{ state_attr('sensor.gamerpower_latest_giveaway', 'open_giveaway_url') }}"
```

## Supported Platforms

- PC
- Steam
- Epic Games Store
- GOG
- itch.io
- Ubisoft
- PlayStation 4/5
- Xbox One/Series X|S
- Nintendo Switch
- Android
- iOS
- VR
- Battle.net
- Origin
- DRM-Free

## Attribution

Data provided by [GamerPower.com](https://www.gamerpower.com)

## License

MIT License - See [LICENSE](LICENSE) for details.
