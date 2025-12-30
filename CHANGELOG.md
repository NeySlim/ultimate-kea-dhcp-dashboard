# Changelog

All notable changes to Ultimate Kea DHCP Dashboard will be documented in this file.

## [1.0.0] - 2025-12-30

### 🎉 Initial Release

#### Features
- **Beautiful UI with 5 Themes**
  - Blossom (default warm pink theme)
  - Dark Mode (sleek dark interface)
  - Neon Pulse (vibrant neon aesthetics)
  - Ocean Breeze (cool blue tones)
  - Netdata (inspired by Netdata monitoring)

- **Real-Time DHCP Monitoring**
  - Live DHCP lease tracking from Kea MySQL backend
  - Automatic hostname resolution
  - MAC address vendor identification
  - Two-table view: DHCP pool and non-pool hosts

- **Advanced Network Scanning**
  - Multi-threaded subnet scanning
  - Individual and global scan control with pause/resume
  - Multiple detection methods: ARP, reverse DNS, SNMP, ping
  - Configurable scan intervals with countdown display
  - Persistent scan state across page refreshes

- **System Monitoring**
  - Real-time CPU usage (per-core gauges)
  - Memory utilization tracking
  - Network I/O monitoring (in/out)
  - Disk usage statistics
  - All metrics update every second

- **Interactive Controls**
  - Theme-aware control icons
  - Global and per-host scan pause/resume buttons
  - Settings panel with live configuration
  - Auto-refresh with visual countdown
  - Smooth animations and transitions

- **Installation & Deployment**
  - Interactive installer with themed UI
  - Automatic dependency installation
  - Systemd service integration
  - Configuration wizard
  - Complete uninstaller

#### Technical Details
- Python 3.8+ backend with Flask
- Vanilla JavaScript frontend
- MySQL database integration
- WebSocket support for real-time updates
- RESTful API endpoints
- Modular codebase structure

#### Configuration
- INI-based configuration file
- Support for multiple subnets
- Customizable scan intervals
- SNMP community configuration
- Database connection settings
- Network range definitions

---

**Full Changelog**: https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/commits/v1.0.0
