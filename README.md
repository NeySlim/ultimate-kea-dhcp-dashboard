# Ultimate Kea DHCP Dashboard

A modern, real-time web dashboard for monitoring ISC Kea DHCP server leases, pools, and network devices with advanced scanning capabilities and system metrics visualization.

## Features

### DHCP Monitoring
- Real-time DHCP lease tracking
- Pool utilization visualization
- Reserved IP management
- MAC address vendor identification
- Automatic hostname resolution

### Network Scanning
- Active device discovery within and outside DHCP pools
- Multi-threaded network scanning for fast results
- Service detection (HTTP/HTTPS)
- Device type identification
- Individual and global scan control

### System Metrics
- Real-time CPU, RAM, Network, and Disk usage
- Responsive gauge visualization
- Theme-aware color schemes
- Per-core CPU monitoring

### Modern UI
- Multiple professional themes (Blossom, Sunset, Ocean, Forest, Night)
- Responsive design
- Real-time auto-refresh
- Pause/resume functionality
- Clean, intuitive interface

## Requirements

- Python 3.8+
- ISC Kea DHCP Server
- Linux system (Debian/Ubuntu recommended)
- Root or sudo access for network scanning

## Quick Installation

```bash
# Download and run the installer
curl -sL https://github.com/NeySlim/ultimate-kea-dashboard/releases/latest/download/install.sh | sudo bash
```

## Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/NeySlim/ultimate-kea-dashboard.git
cd ultimate-kea-dashboard
```

2. Install dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip nmap arping
```

3. Configure the dashboard:
```bash
sudo cp etc/ultimate-dashboard.conf.example etc/ultimate-dashboard.conf
sudo nano etc/ultimate-dashboard.conf
```

4. Run the dashboard:
```bash
sudo python3 bin/ultimate-dashboard
```

Or install as a systemd service:
```bash
sudo ./install.sh
```

## Configuration

Edit `/etc/ultimate-dashboard/ultimate-dashboard.conf`:

```ini
[DEFAULT]
# Server settings
port = 8089
ssl_enabled = true

# Kea paths
kea_config = /etc/kea/kea-dhcp4.conf
kea_leases = /var/lib/kea/kea-leases4.csv

# Network settings
subnet = 192.168.1.0/24
dhcp_range_start = 192.168.1.100
dhcp_range_end = 192.168.1.200

# Scanning
scan_threads = 50
scan_timeout = 0.5
```

## Usage

Access the dashboard at:
- HTTPS: `https://your-server-ip:8089`
- HTTP: `http://your-server-ip:8089` (if SSL disabled)

### Controls

- **Global Scan Control**: Pause/resume all network scans from the header
- **Individual Scan Control**: Pause/resume scanning for specific devices
- **Theme Selector**: Choose from 5 professional themes
- **Auto-refresh**: Configurable refresh interval (default: 30s)

## Architecture

```
ultimate-kea-dashboard/
├── bin/
│   └── ultimate-dashboard          # Main application
├── lib/
│   ├── themes.py                   # Theme definitions
│   ├── stats.py                    # System metrics
│   ├── network_scanner.py          # Network scanning logic
│   ├── device_detection.py         # Device type detection
│   └── mac_vendor.py               # MAC vendor lookup
├── static/
│   └── js/
│       └── gauges.js               # Gauge visualization
├── data/
│   └── oui.json                    # IEEE OUI database
└── etc/
    └── ultimate-dashboard.conf.example
```

## Security Considerations

- SSL/TLS encryption enabled by default
- Configuration file should be readable only by root
- No default passwords or credentials
- Network scanning requires appropriate permissions

## Performance

- Multi-threaded scanning (configurable thread pool)
- Efficient caching mechanisms
- Minimal resource footprint
- Optimized for networks with 100+ devices

## Troubleshooting

### Dashboard not starting
```bash
# Check logs
sudo journalctl -u ultimate-dashboard -f

# Verify configuration
sudo python3 -c "import configparser; c=configparser.ConfigParser(); c.read('/etc/ultimate-dashboard/ultimate-dashboard.conf'); print('Config OK')"
```

### Scans not working
```bash
# Ensure required tools are installed
which nmap arping

# Check permissions
sudo -v
```

### Empty MAC addresses
- Ensure ARP table is populated (ping devices first)
- Run dashboard with sudo/root privileges
- Check network interface permissions

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Author

Created and maintained by NeySlim.

## Acknowledgments

- ISC Kea DHCP Server team
- IEEE for OUI database
- Netdata for UI inspiration
