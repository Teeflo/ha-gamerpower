# GamerPower Giveaways for Home Assistant

[![GitHub Release](https://img.shields.io/github/v/release/Teeflo/ha-gamerpower?style=for-the-badge)](https://github.com/Teeflo/ha-gamerpower/releases)
[![GitHub Downloads](https://img.shields.io/github/downloads/Teeflo/ha-gamerpower/total?style=for-the-badge&color=blue)](https://github.com/Teeflo/ha-gamerpower/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/Teeflo/ha-gamerpower?style=for-the-badge)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue?style=for-the-badge&logo=home-assistant)](https://www.home-assistant.io/)

---

**Never miss a free game again!** This integration automatically tracks free games and giveaways from GamerPower.

## ✨ Features

- 🎮 **Track Free Games & Giveaways** - Automatically fetch active giveaways
- 🔍 **Platform Filtering** - Filter by Steam, Epic Games, PlayStation, Xbox, and more
- 📊 **Type Filtering** - Filter by Full Games, In-Game Loot, or Beta Access
- 💰 **Worth Estimation** - See the total estimated value of active giveaways
- 🔔 **New Giveaway Detection** - Get notified when new giveaways appear
- ⏱️ **Configurable Updates** - Set check intervals from 5 minutes to 24 hours

## 📦 Installation

### HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click the **⋮** menu → **Custom repositories**
4. Add: `https://github.com/Teeflo/ha-gamerpower`
5. Select **Integration** as category
6. Click **Install**
7. **Restart** Home Assistant

### Manual Installation

1. Download the latest release from [GitHub Releases](https://github.com/Teeflo/ha-gamerpower/releases)
2. Extract `custom_components/gamerpower` to your `config/custom_components/` directory
3. Restart Home Assistant

## ⚙️ Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for **"GamerPower Giveaways"**
3. Configure your preferred platforms and giveaway types
4. Set your desired update interval

## 📊 Available Sensors

| Sensor | Description |
|--------|-------------|
| `sensor.gamerpower_total_giveaways` | Total number of active giveaways |
| `sensor.gamerpower_total_worth` | Total estimated value in USD |
| `sensor.gamerpower_latest_giveaway` | Latest giveaway with full details |
| `sensor.gamerpower_active_giveaways_list` | Complete list with platform grouping |

## 🎯 Services

### `gamerpower.refresh`
Manually refresh giveaway data.

### `gamerpower.get_giveaway`
Get detailed information about a specific giveaway by ID.

```yaml
service: gamerpower.get_giveaway
data:
  giveaway_id: 525
```

## 🤖 Automation Examples

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
          title: "🎮 New Free Game!"
          message: "{{ states('sensor.gamerpower_latest_giveaway') }}"
          data:
            url: "{{ state_attr('sensor.gamerpower_latest_giveaway', 'open_giveaway_url') }}"
```

### Daily Giveaway Summary

```yaml
automation:
  - alias: "Daily Giveaway Summary"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "🎁 Daily Giveaway Summary"
          message: >
            {{ states('sensor.gamerpower_total_giveaways') }} active giveaways
            worth ~${{ states('sensor.gamerpower_total_worth') }}
```

## 🎮 Supported Platforms

| Platform | Key |
|----------|-----|
| PC | `pc` |
| Steam | `steam` |
| Epic Games Store | `epic-games-store` |
| GOG | `gog` |
| itch.io | `itchio` |
| Ubisoft | `ubisoft` |
| PlayStation 4 | `ps4` |
| PlayStation 5 | `ps5` |
| Xbox One | `xbox-one` |
| Xbox Series X\|S | `xbox-series-xs` |
| Nintendo Switch | `switch` |
| Android | `android` |
| iOS | `ios` |
| VR | `vr` |
| Battle.net | `battlenet` |
| Origin | `origin` |
| DRM-Free | `drm-free` |

## 📝 Changelog

See [Releases](https://github.com/Teeflo/ha-gamerpower/releases) for the changelog.

## 🙏 Attribution

Data provided by [GamerPower.com](https://www.gamerpower.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <a href="https://github.com/Teeflo/ha-gamerpower">
    <img src="images/logo.png" alt="GamerPower Logo" height="100">
  </a>
</p>
<p align="center">
  Made with ❤️ for the Home Assistant community
</p>
