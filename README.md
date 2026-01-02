# Ultimate Kea DHCP Dashboard

> **Languages / Langues:** [🇬🇧 English](README.md) | [🇫🇷 Français](README.fr.md)

---

A modern, real-time web dashboard for ISC Kea DHCP server with advanced network discovery, SNMP monitoring, and system metrics.

![Dashboard Screenshot](docs/images/dashboard-screenshot.png)

## Key Features

- **DHCP Monitoring**: Real-time lease tracking, pool utilization, MAC vendor identification (IEEE OUI)
- **Network Discovery**: Multi-threaded scanning, service detection (SSH/HTTP/SNMP), device type identification
- **SNMP Integration**: System information discovery (sysDescr, sysContact, sysLocation, sysUpTime), configurable communities
- **System Metrics**: Real-time CPU/RAM/Network/Disk monitoring with responsive gauges
- **Modern UI**: 7 themes (Ember, Twilight, Frost, Blossom, Clarity, Pulse, Vicuna), 5 languages, responsive design
- **Auto-Update**: Built-in update checker and one-click updates from GitHub releases

## Requirements

- Python 3.8+
- ISC Kea DHCP Server
- Linux system (multiple distributions supported)
- Root or sudo access for network scanning

### Supported Linux Distributions

- **Debian/Ubuntu** (APT)
- **Fedora/CentOS/RHEL/Rocky/AlmaLinux** (DNF/YUM)
- **Arch/Manjaro** (Pacman)
- **openSUSE/SLES** (Zypper)

See [Supported Distributions](docs/DISTRIBUTIONS.md) for detailed compatibility information.

## Installation

### Automated Installer (Recommended)

```bash
curl -sL https://github.com/NeySlim/ultimate-kea-dhcp-dashboard/releases/latest/download/ultimate-kea-dashboard-installer.sh -o installer.sh
sudo bash installer.sh
```

### Distribution Packages

Download `.deb`, `.rpm`, or `.pkg.tar.zst` from [releases](https://github.com/NeySlim/ultimate-kea-dhcp-dashboard/releases):

```bash
# Debian/Ubuntu
sudo dpkg -i ultimate-kea-dashboard_*.deb && sudo apt-get install -f

# Fedora/RHEL
sudo dnf install ultimate-kea-dashboard-*.rpm

# Arch Linux
sudo pacman -U ultimate-kea-dashboard-*.pkg.tar.zst
```

### Manual Installation

```bash
git clone https://github.com/NeySlim/ultimate-kea-dhcp-dashboard.git
cd ultimate-kea-dhcp-dashboard
sudo bash install.sh
```


## Configuration

Edit `/opt/ultimate-kea-dashboard/etc/ultimate-kea-dashboard.conf`:

```ini
[DEFAULT]
port = 8089
ssl_enabled = true
kea_socket = /run/kea/kea4-ctrl-socket
scan_threads = 50
snmp_enabled = true
snmp_communities = public,home
```

Configuration is automatically retrieved from Kea via control socket—no manual subnet/pool setup needed!

## Usage

Access at `https://your-server:8089` (or HTTP if SSL disabled)

- **Settings**: Configure refresh intervals, themes, languages
- **Scan Control**: Pause/resume network discovery
- **Auto-Update**: Built-in update checker with one-click updates

## Documentation

- [Installation Guides](docs/) - Distribution-specific instructions
- [Dependencies](docs/DEPENDENCIES.md) - Complete dependency list
- [Themes](THEME.md) - Theme customization
- [SNMP](SNMP-FEATURE.md) - SNMP configuration

## License

MIT License - See [LICENSE](LICENSE) for details.

## Links

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
