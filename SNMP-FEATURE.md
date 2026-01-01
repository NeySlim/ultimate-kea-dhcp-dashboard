# SNMP System Discovery Feature

## Overview
Enhanced SNMP discovery feature that retrieves comprehensive system information from network devices.

## Features

### Multi-Community Support
- Configure multiple SNMP communities via comma-separated list
- Tries each community in order until successful
- Default: `public`
- Production config: `public,home`

### Information Collected
When SNMP is available on a device, the following information is retrieved:
- **sysName**: System hostname
- **sysDescr**: Detailed system description
- **sysUpTime**: Device uptime
- **sysContact**: System contact information
- **sysLocation**: Physical location

### Configuration

In `ultimate-dashboard.conf` or `/etc/ultimate-dashboard/ultimate-dashboard.conf`:

```ini
[DEFAULT]
enable_snmp = true
snmp_communities = public,home
snmp_timeout = 1
```

### Display

SNMP information is displayed in the dashboard under the "Scan Status" column for static devices:

- Green bordered box with 📡 SNMP icon
- Shows discovered system information
- Only appears when SNMP is successfully queried

### Implementation Details

**Files Modified:**
- `lib/network_scanner.py`: Added `get_snmp_system_info()` function
- `bin/ultimate-dashboard`: Integrated SNMP display in static devices table
- `lib/config.py`: Support for `snmp_communities` list
- `data/translations.json`: Added SNMP-related translations (all 5 languages)
- `etc/ultimate-dashboard.conf.example`: Updated example configuration

**Functions:**
- `get_snmp_system_info(ip, communities, timeout)`: Main SNMP query function
- Returns dict with SNMP data or None if unavailable
- Uses SNMPv2c protocol
- Requires `snmpget` command (from `snmp` package)

### Usage Example

```python
from network_scanner import get_snmp_system_info

info = get_snmp_system_info('192.168.1.1', ['public', 'home'], timeout=1)
if info and info.get('available'):
    print(f"System: {info.get('sysDescr')}")
    print(f"Uptime: {info.get('sysUpTime')}")
    print(f"Location: {info.get('sysLocation')}")
```

## Testing

To test SNMP on a device:
```bash
snmpget -v2c -c public -Oqv <IP> 1.3.6.1.2.1.1.5.0
```

## Dependencies

Requires `snmp` package:
- Debian/Ubuntu: `apt install snmp`
- Fedora/RHEL: `dnf install net-snmp-utils`
- Arch: `pacman -S net-snmp`
