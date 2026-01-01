# Changelog

## [1.2.0] - 2026-01-01 - Multi-Distribution Support

### Distribution Support
- **ADDED**: Multi-distribution installer with automatic detection
  - Debian/Ubuntu (APT)
  - Fedora/CentOS/RHEL/Rocky/AlmaLinux (DNF/YUM)
  - Arch/Manjaro (Pacman)
  - openSUSE/SLES (Zypper)
- **ADDED**: Automatic package manager detection and configuration
- **ADDED**: Distribution-specific default SSL certificate paths
- **IMPROVED**: Enhanced compatibility across Linux distributions

### Dependencies
- **ADDED**: Optional dependencies for advanced features
  - SNMP utilities (snmp, net-snmp-utils, net-snmp)
  - Avahi/mDNS tools (avahi-utils, avahi-tools, avahi)
- **ADDED**: **psutil** installation via **system package managers** (python3-psutil, python-psutil)
  - Debian/Ubuntu: python3-psutil
  - Fedora/RHEL/CentOS: python3-psutil (via EPEL)
  - Arch: python-psutil
  - openSUSE: python3-psutil
- **IMPROVED**: Use native packages instead of pip to respect PEP 668 and avoid conflicts
- **ADDED**: Graceful degradation when optional packages are missing
- **ADDED**: net-tools package for ARP command support
- **IMPROVED**: Dependency installation with clear warnings for optional packages
- **UPDATED**: requirements.txt with system package recommendations
- **CREATED**: check-dependencies.sh script to verify all dependencies

### Documentation
- **ADDED**: Comprehensive distribution support documentation (`docs/DISTRIBUTIONS.md`)
- **ADDED**: Fedora-specific installation guide (`docs/INSTALL-FEDORA.md`)
- **ADDED**: Arch Linux-specific installation guide (`docs/INSTALL-ARCH.md`)
- **ADDED**: Dependencies documentation (`docs/DEPENDENCIES.md`)
- **ADDED**: Multi-distribution developer guide (`docs/MULTI-DISTRO-DEV.md`)
- **UPDATED**: README.md with multi-distribution installation instructions
- **ADDED**: Firewall configuration guides for different distributions
- **ADDED**: SELinux configuration notes for RHEL-based systems

### Installation Improvements
- **ENHANCED**: `install.sh` now detects Linux distribution automatically
- **ADDED**: Package manager abstraction layer
- **ADDED**: Distribution-specific dependency installation
- **IMPROVED**: SSL certificate path defaults based on distribution
- **REMOVED**: Debian/Ubuntu-only restriction
- **ADDED**: Warning messages for optional packages installation failures

### Compatibility
- **VERIFIED**: Standard Kea DHCP paths work across all distributions
  - `/etc/kea/` for configuration
  - `/var/lib/kea/` for leases
  - `/run/kea/` for control socket
- **VERIFIED**: FHS-compliant installation paths
- **TESTED**: Command availability across distributions

## [1.1.0] - 2025-12-31 - Major Feature & UX Enhancements

### Configuration Simplification
- **REMOVED**: Manual subnet and DHCP range configuration requirements
- **ADDED**: Automatic subnet and pool retrieval directly from Kea via control socket
- **IMPROVED**: Socket-first architecture - lease file now used only as fallback
- **SIMPLIFIED**: Configuration file significantly reduced - just point to Kea config and socket

### UI/UX Improvements
- **ADDED**: Custom SVG icon system replacing emoji for device types
  - Created 11 device-type icons (server, desktop, laptop, mobile, tablet, IoT, printer, camera, router, TV, unknown)
  - Created 5 service icons (SSH, HTTP, HTTPS, SNMP, generic)
  - All icons are theme-aware and adapt to current color scheme
  - Proper sizing and stroke width for professional appearance
- **ADDED**: 6 professional theme variants (Ember, Twilight, Frost, Blossom, Clarity, Pulse)
- **FIXED**: Emoji flash on initial page load - SVG icons now display immediately
- **IMPROVED**: Icon rendering with proper fallback system
- **OPTIMIZED**: Service display formatting with icon badges

### Performance & Refresh System
- **REMOVED**: Global page refresh setting (caused data inconsistency)
- **FIXED**: Refresh synchronization issues between different components
- **IMPROVED**: Table-based API refresh instead of full page reload
- **STANDARDIZED**: 1-second refresh rate for all real-time data
- **FIXED**: Countdown timer now properly synchronized with actual data refresh

### Translation & Localization
- **FIXED**: Missing translations for "No service" / "Aucun service"
- **IMPROVED**: Complete translation coverage across all UI elements
- **VERIFIED**: All 5 languages (EN, FR, ES, DE, TH) properly implemented

### Documentation
- **ADDED**: Professional anonymized dashboard screenshot
- **UPDATED**: README with new features and simplified configuration
- **IMPROVED**: Feature descriptions to reflect actual capabilities
- **ADDED**: Architecture explanations for socket-based retrieval

### Technical Improvements
- **REFACTORED**: Icon rendering system for consistency
- **OPTIMIZED**: Data refresh logic for better performance
- **REMOVED**: Redundant refresh configuration options
- **IMPROVED**: Error handling for icon fallbacks

## [1.0.0] - 2024-12-31 - Code Professionalization

### Security
- **BREAKING**: Anonymized default credentials in configuration files
  - Changed `snmp_community` from `home` to `public` (placeholder)
  - Changed SSL certificate paths to placeholders
  - Added `.gitignore` to prevent committing sensitive files
  - Created example configuration file

### Code Quality & Architecture
- **Modularized codebase**: Split monolithic file into focused modules
  - `lib/network_scanner.py` - Network scanning and service discovery (173 lines)
  - `lib/device_detection.py` - Device type classification (190 lines)
  - `lib/mac_vendor.py` - MAC vendor lookup utilities (67 lines)
  - `lib/stats.py` - System statistics (existing, 78 lines)
  - `lib/themes.py` - UI themes (existing, 152 lines)
  
- **Removed code duplication**: Eliminated ~350 lines of duplicate functions
- **Fixed code errors**: Corrected malformed function definitions
- **Improved imports**: Clean module imports in main application

### Documentation
- **README.md**: Rewritten with professional, factual descriptions
  - Clear feature list with technical details
  - Structured installation and configuration instructions
  - Security considerations section
  - Architecture overview
  
- **INSTALL.md**: Comprehensive installation guide (new)
  - Step-by-step setup instructions
  - Systemd service configuration
  - SSL/TLS setup guide
  - Troubleshooting section
  
- **CONTRIBUTING.md**: Development and contribution guidelines (new)
  - Code organization documentation
  - Style guidelines
  - Security best practices
  - Pull request guidelines
  
- **LICENSE**: Added MIT License (new)
- **CHANGELOG.md**: This file (new)

### Configuration
- Reduced emoji usage in documentation (professional tone)
- Created `ultimate-dashboard.conf.example` for safe distribution
- Updated default SNMP community string to standard value

### Project Structure
```
ultimate-dashboard/
├── bin/ultimate-dashboard       (2712 lines - cleaned & modularized)
├── lib/                         (660 lines total - 5 modules)
├── etc/*.conf.example           (configuration template)
├── .gitignore                   (security)
├── LICENSE                      (legal)
├── README.md                    (professional overview)
├── INSTALL.md                   (setup guide)
├── CONTRIBUTING.md              (development guide)
└── CHANGELOG.md                 (version history)
```

### Metrics
- **Total codebase**: 3372 lines (down from ~3700 with deduplication)
- **Main file**: Reduced by ~500 lines through modularization
- **New modules**: 5 focused, reusable components
- **Documentation**: 4 comprehensive guides added
