# Ultimate Kea DHCP Dashboard

A beautiful, real-time monitoring dashboard for Kea DHCP servers with advanced network scanning and system monitoring capabilities.

![Dashboard Preview](https://img.shields.io/badge/Status-Production-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

## ✨ Features

### 🎨 Beautiful Themes
- **5 stunning themes**: Blossom (default), Dark Mode, Neon Pulse, Ocean Breeze, and Netdata-inspired
- Fully themed UI components including gauges, buttons, and tables
- Smooth transitions and modern design

### 📊 Real-Time Monitoring
- **DHCP Lease Tracking**: Monitor all active DHCP leases with hostname resolution
- **Network Scanning**: Automatic scanning of DHCP pool and non-DHCP subnets
- **System Metrics**: CPU, RAM, Network, and Disk usage with beautiful gauge displays
- **Live Updates**: Auto-refresh with configurable intervals

### 🔧 Advanced Features
- **Individual & Global Scan Control**: Pause/resume scanning globally or per-host
- **Multiple Data Sources**: ARP, reverse DNS, SNMP, and ping for comprehensive host information
- **MAC Address Vendor Lookup**: Identify device manufacturers
- **Hostname Resolution**: Multiple methods for accurate hostname detection
- **Persistent Settings**: All preferences saved automatically

### 🖥️ System Requirements
- Debian-based Linux (Debian, Ubuntu, etc.)
- Python 3.8 or higher
- Kea DHCP Server with MySQL backend
- Root or sudo access for installation

## 🚀 Quick Install

```bash
# Download and run the installer
curl -fsSL https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/releases/latest/download/install.sh | sudo bash
```

Or manual installation:

```bash
# Download the installer
wget https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/releases/latest/download/install.sh

# Make it executable
chmod +x install.sh

# Run the installer
sudo ./install.sh
```

## 📦 What's Included

- Interactive installation wizard with theme-based UI
- Automatic dependency installation
- Service configuration and auto-start
- Configuration file generation
- Complete uninstallation support

## 🔧 Configuration

During installation, you'll be prompted for:

- **Kea Database Settings**: Host, port, database name, credentials
- **Network Configuration**: DHCP pool range, subnet, reserved IPs
- **Dashboard Settings**: Port, refresh interval, auto-scan on startup
- **SNMP Community**: For enhanced device information (optional)

All settings can be reconfigured later by editing `/opt/ultimate-dashboard/etc/config.ini`

## 🎯 Usage

After installation, the dashboard will be available at:

```
http://YOUR_SERVER_IP:8089
```

### Service Management

```bash
# Check status
sudo systemctl status ultimate-dashboard

# Start/Stop/Restart
sudo systemctl start ultimate-dashboard
sudo systemctl stop ultimate-dashboard
sudo systemctl restart ultimate-dashboard

# View logs
sudo journalctl -u ultimate-dashboard -f
```

### Uninstall

```bash
sudo /opt/ultimate-dashboard/bin/uninstall.sh
```

## 🎨 Themes

### Blossom (Default)
Warm, pink-themed interface with soft gradients

### Dark Mode
Sleek dark theme for reduced eye strain

### Neon Pulse
Vibrant purple and cyan neon aesthetics

### Ocean Breeze
Cool blue tones inspired by the ocean

### Netdata
Faithful recreation of Netdata's monitoring interface

## 🛠️ Technical Details

### Architecture
- **Backend**: Python 3 with Flask web framework
- **Frontend**: Vanilla JavaScript with real-time updates
- **Database**: MySQL for Kea DHCP lease data
- **WebSockets**: Real-time communication for live metrics

### Network Scanning
- Multi-threaded scanning for performance
- ARP table integration
- Reverse DNS lookups
- SNMP device queries
- ICMP ping checks

### System Monitoring
- Per-core CPU usage tracking
- Real-time memory statistics
- Network I/O monitoring (in/out)
- Disk usage with GB metrics

## 📄 License

MIT License - Feel free to use, modify, and distribute

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📧 Support

For issues and questions:
- GitHub Issues: [Report a bug](https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/issues)
- Discussions: [Ask questions](https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/discussions)

## 🙏 Acknowledgments

- Inspired by Netdata's beautiful monitoring interface
- Built for the Kea DHCP community
- Theme designs influenced by modern UI trends

## 📸 Screenshots

### Main Dashboard
![Main Dashboard](screenshots/dashboard-main.png)

### System Metrics
![System Metrics](screenshots/metrics.png)

### Theme Selection
![Themes](screenshots/themes.png)

---

**Made with ❤️ for network administrators**
# ultimate-kea-dhcp-dashboard
