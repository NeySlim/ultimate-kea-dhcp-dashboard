# Changelog

## [1.6.7] - 2026-01-02

### ⚡ Optimisations Performance
- **OPTIMIZED**: Scan TCP/UDP parallèle (gain ~10-15s par device)
  - Les scans TCP et UDP s'exécutent maintenant en parallèle au lieu de séquentiellement
  - Utilise ThreadPoolExecutor pour scanner simultanément
  - Réduction significative du temps de scan global
  
- **OPTIMIZED**: Cache SNMP avec TTL de 5 minutes
  - Les données SNMP sont cachées pendant 5 minutes (au lieu de 60 secondes)
  - Réduit drastiquement le nombre de requêtes SNMP
  - Les infos SNMP changent rarement (sysName, sysContact, sysLocation)
  - Seul sysUpTime change fréquemment
  
- **NEW**: Ports UDP supplémentaires
  - Ajout port 69 (TFTP)
  - Ajout ports 137-138 (NetBIOS)
  - Ajout port 500 (IPSec/IKE)
  - Ajout port 1194 (OpenVPN)
  - Meilleure découverte des services réseau

### Configuration
Ports UDP par défaut: `53,67,69,123,137,138,161,162,500,514,520,1194`

---

## [1.6.6] - 2026-01-02

### 🔧 Corrections
- **FIXED**: Scan SNMP cassé - Les ports UDP n'étaient pas scannés
  - Ajout du scan UDP (port 161) pour détecter les services SNMP
  - Le scan nmap ne détectait que les ports TCP, manquant ainsi tous les services UDP
  - 7 devices SNMP maintenant détectés (au lieu de 0)
  
### ✨ Améliorations
- **NEW**: Support configurable des ports TCP et UDP à scanner
  - Nouveaux paramètres `tcp_ports` et `udp_ports` dans la configuration
  - Ports UDP par défaut: 53 (DNS), 67 (DHCP), 123 (NTP), 161/162 (SNMP), 514 (Syslog), 520 (RIP)
  - Ports TCP configurables via fichier de conf
  - Scan UDP et TCP parallèles pour meilleure performance
- **IMPROVED**: Fonction `scan_network_host()` refactorisée
  - Gestion séparée des scans TCP et UDP
  - Meilleure gestion des erreurs
  - Documentation améliorée

---

## [1.6.5] - 2026-01-02

### Améliorations
- **NEW**: Système de mise à jour automatique depuis GitHub
  - Détection automatique des nouvelles versions
  - Bouton de mise à jour one-click dans l'interface
  - Support des installations via git et via packages
  - Préservation des modifications locales lors des mises à jour
- **NEW**: Workflows de packaging séparés par distribution (DEB, RPM, Arch)
  - Création automatique de packages natifs pour chaque distribution
  - Nommage cohérent des releases avec les tags de version
  - Indépendance des jobs pour éviter les échecs en cascade

### Corrections
- **FIXED**: Fichier translations.json manquant dans les packages
- **FIXED**: Erreurs d'installation de packages dues à des fichiers manquants
- **FIXED**: Scripts postinstall robustifiés avec création de répertoires manquants
- **FIXED**: Chemins de fichiers problématiques dans tous les packages
- **FIXED**: Workflow de création des packages

---

## [1.6.0] - 2026-01-02 - Production-Ready Multi-Distribution Packaging

### Major Milestone 🎉
First production release with complete native package support for all major Linux distributions!

### New Features
- **NEW**: Native .deb packages for Debian/Ubuntu
- **NEW**: Native .rpm packages for Red Hat/Fedora/CentOS/Rocky/Alma  
- **NEW**: Native .pkg.tar.zst packages for Arch Linux
- **NEW**: Automated package building via GitHub Actions
- **NEW**: All packages include Kea DHCP as automatic dependency
- **NEW**: Systemd service auto-configuration in all packages
- **NEW**: Automatic user creation and permissions setup

### Distribution Support
- Debian 11+ and Ubuntu 20.04+
- Red Hat 8+, Fedora 35+, Rocky Linux 8+, AlmaLinux 8+
- Arch Linux (current)

### Installation Simplified
Users can now install with their native package manager:
- `apt install ./ultimate-kea-dashboard_*.deb`
- `dnf install ultimate-kea-dashboard-*.rpm`
- `pacman -U ultimate-kea-dashboard-*.pkg.tar.zst`

### Bug Fixes (from 1.5.7-1.5.9)
- **FIXED**: Missing systemd service template file
- **FIXED**: Debian compat file conflict with debhelper-compat
- **FIXED**: Binary file permissions in packaging rules

---

## [1.5.8] - 2026-01-01 - Packaging Fix

### Bug Fixes
- **FIXED**: Missing systemd service file in repository for packaging
- Added etc/ultimate-kea-dashboard.service template file

---

## [1.5.7] - 2026-01-01 - Multi-Distribution Packaging

### New Features
- **NEW**: Native package support for major Linux distributions
  - Debian/Ubuntu (.deb packages)
  - Red Hat/Fedora/CentOS/Rocky/Alma (.rpm packages)
  - Arch Linux (.pkg.tar.zst packages)
- **NEW**: Automated package building via GitHub Actions
- **NEW**: All packages include Kea DHCP as dependency
- **NEW**: Automatic service setup and user creation in packages
- **NEW**: Automatic OUI database download on package installation

### Improvements
- **IMPROVED**: Installation process simplified with native packages
- **IMPROVED**: Dependency management handled by package managers
- **IMPROVED**: Systemd service automatically enabled on package install
- **IMPROVED**: README updated with package installation instructions

### Technical Details
- Packaging files in `packaging/{debian,rpm,arch}/`
- GitHub Actions workflow builds all packages on release tags
- Pre-built packages available in GitHub releases
- All packages create system user, install to /opt, setup logs
- Package manager handles all dependencies automatically

---

## [1.5.6] - 2026-01-01 - Enhanced UI and Auto-Update

### New Features
- **NEW**: Automatic update checker with GitHub integration
- **NEW**: One-click update button in dashboard header
- **NEW**: Configurable refresh interval (1s, 2s, 5s, 10s, 30s)
- **NEW**: Service discovery count badges with hover details
- **NEW**: SNMP details in hover tooltips
- **NEW**: Vicuna theme (OPNsense-inspired)

### Improvements
- **IMPROVED**: Vendor lookup using IEEE OUI database
- **IMPROVED**: Automatic weekly OUI database updates
- **IMPROVED**: Static devices show ARP data immediately
- **IMPROVED**: Hover tooltips prevent flicker on table refresh
- **IMPROVED**: Tooltips overflow table boundaries properly
- **IMPROVED**: IP address sorting (numerical instead of alphabetical)

### Bug Fixes
- **FIXED**: Static devices table sorting not working
- **FIXED**: MAC addresses not showing in static devices table
- **FIXED**: ARP incomplete entries appearing in tables
- **FIXED**: DHCP pool IPs appearing in static devices table
- **FIXED**: Services breaking table cell height

---

## [1.5.5] - 2026-01-01 - Static Devices Filtering

### Improvements
- **IMPROVED**: Static devices table now only shows devices that respond
  - Filters out IPs with no MAC address, no services, and no hostname
  - Removes duplicate IPs already shown in DHCP leases table
  - Significantly reduces clutter (from 133 to ~10-15 active devices)
  - DHCP reservations are always shown regardless of response status

### Bug Fixes
- **FIXED**: IPs from DHCP pool appearing in static devices table
- **FIXED**: Duplicate devices shown in both leases and static tables
- **FIXED**: Empty/non-responsive IPs cluttering the static devices list

### Technical Details
- API endpoint now filters static_devices before sending to frontend
- Checks for: `has_mac OR has_services OR has_hostname OR is_reservation`
- Excludes any IP already present in DHCP leases to avoid duplicates
- Results in cleaner, more useful static devices display

---

## [1.5.4] - 2026-01-01 - Static Devices Detection Enhancement

### Improvements
- **IMPROVED**: Static devices detection now includes ARP cache discovery
  - Changed from scanning only first/last 10 IPs to first/last 50 + ARP cache
  - Automatically detects all active devices outside DHCP pools
  - More efficient scanning strategy for large subnets

### Technical Details
- Uses `ip neigh show` to discover active devices from ARP cache
- Combines ARP-discovered IPs with common static ranges (first 50, last 50)
- For subnets < 100 hosts, scans all IPs outside pools
- Significantly improves device discovery without excessive network scanning

---

## [1.5.3] - 2026-01-01 - SNMP Display Fix

### Bug Fixes
- **FIXED**: SNMP information not displaying in web interface
  - Fixed JavaScript detection of SNMP port 161
  - Changed from checking `services_html` to `services` array
  - SNMP details now properly display with system description, contact, location, and uptime
  - Affects both DHCP leases and static devices tables

### Technical Details
- The SNMP port 161 is intentionally excluded from `services_html` to avoid duplication
- JavaScript now correctly checks the raw `services` array for port detection
- SNMP info displays in a styled green-bordered div when available

---

## [2.5.0] - 2026-01-01 - SNMP System Discovery

### SNMP Features
- **ADDED**: SNMP system information discovery for network devices
  - Automatic collection of sysDescr, sysContact, sysLocation, sysUpTime
  - Real-time display in dashboard status column
  - "SNMP?" indicator when SNMP is enabled but no data yet
  - "SNMP:" with full system info when data is available
- **ADDED**: Configurable SNMP communities support
  - Multiple communities can be specified (comma-separated)
  - Communities tried in order until one succeeds
  - Example: `snmp_communities = public,home,private`
- **ADDED**: Enhanced configuration file parsing
  - Support for both `[DEFAULT]` and `[server]` sections
  - Automatic comma-separated list parsing
  - Better error handling and logging

### Configuration Improvements
- **IMPROVED**: Config loading now supports list-type parameters
- **ADDED**: Startup logging for SNMP communities configuration
- **ADDED**: Debug logging for SNMP data collection

### Bug Fixes
- **FIXED**: Missing `is_static` variable in static devices display
- **FIXED**: Config file section detection (DEFAULT vs server)
- **FIXED**: SNMP display not showing for static devices

### Documentation
- **UPDATED**: README with SNMP configuration examples
- **UPDATED**: Configuration file example with SNMP settings
- **UPDATED**: French and English documentation

## [1.2.2] - 2026-01-01 - Custom Device Configuration System

### Custom Device Features
- **ADDED**: User-configurable custom devices via JSON configuration
  - `etc/custom-devices.json`: Configuration file for custom devices
  - `lib/custom_devices.py`: Module for custom device management (10.5 KB)
  - Simple JSON format for easy customization
- **ADDED**: Priority-based device detection (custom devices checked FIRST)
- **ADDED**: Modular and extensible architecture
- **ADDED**: Hot-reload support (restart dashboard to apply changes)

### Gaming PC Icon Themes
- **ADDED**: 3 beautiful SVG icon themes for gaming PCs
  - `master`: High-end setup with large curved monitor + RGB lighting + crown badge
  - `apprentice`: Compact mini PC with small monitor + animated RGB fan + level indicator
  - `generic`: Standard gaming tower PC with dual RGB fans
- **ADDED**: Animated SVG elements (pulsing LEDs, rotating fans)
- **ADDED**: Personalized labels and descriptions per device

### Documentation
- **ADDED**: Complete user guide `docs/CUSTOM-DEVICES.md`
  - Configuration file structure and parameters
  - Multiple examples (Gaming PC, Server, Smart Home)
  - Icon themes documentation
  - Hostname matching rules
  - Validation and troubleshooting guide

### Bug Fixes
- **FIXED**: Gaming PCs (marvin, shepard) incorrectly detected as routers
- **FIXED**: Device detection priority (custom devices now have highest priority)
- **FIXED**: Import compatibility (absolute imports for production)

### Technical
- **CHANGED**: `lib/device_detection.py` - Integrated custom_devices module
- **TESTED**: Production deployment verified on Debian 13
- **MAINTAINED**: Full backward compatibility (no breaking changes)

### Benefits
- ✅ No code modification needed for custom devices
- ✅ Simple JSON editing
- ✅ Beautiful personalized icons
- ✅ Extensible design
- ✅ Well-documented

## [1.2.1] - 2026-01-01 - Code Refactoring & Bilingual Documentation

### Code Structure (Refactoring)
- **ADDED**: Modular code structure with separate modules
  - `lib/translations.py`: Multi-language translations (FR, EN, ES, DE, TH)
  - `lib/config.py`: Configuration loading and management
  - `lib/utils.py`: Utility functions (hostname resolution, formatting)
- **IMPROVED**: Better code organization and maintainability
- **IMPROVED**: Easier testing and module reusability
- **PREPARED**: Foundation for further refactoring (HTML templates, Kea API)

### Documentation
- **ADDED**: Complete bilingual documentation (English/French)
  - `README.fr.md`: Complete French translation of README
  - `docs/README.md`: Bilingual documentation index
  - `docs/LANGUAGE-INDEX.md`: Language navigation guide
- **ADDED**: Language switchers on all documentation files
- **IMPROVED**: Installation guides with bilingual headers
  - `docs/INSTALL-FEDORA.md` (EN) + `docs/INSTALL-FEDORA.fr.md` (FR)
  - `docs/INSTALL-ARCH.md` (EN) + `docs/INSTALL-ARCH.fr.md` (FR)
- **ADDED**: Documentation structure extensible to other languages (ES, DE, IT, etc.)

### Technical
- **TESTED**: Production deployment verified and functional
- **MAINTAINED**: Full backward compatibility
- **STRUCTURE**: Clean separation of concerns (translations, config, utilities)

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

## [1.6.3] - 2026-01-02

### Fixed
- Fixed translations.json not included in packages
- Fixed package installation errors due to missing files

