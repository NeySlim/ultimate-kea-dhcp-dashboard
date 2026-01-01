# Supported Linux Distributions

Ultimate Kea DHCP Dashboard supports multiple Linux distributions with automatic detection and configuration.

## Officially Supported Distributions

### Debian-based
- **Debian** 10+ (Buster, Bullseye, Bookworm)
- **Ubuntu** 20.04+ (Focal, Jammy, Noble)
- **Linux Mint** 20+
- **Pop!_OS** 20.04+

**Package Manager**: APT

**Required Dependencies**: `nmap`, `arping`, `python3`, `python3-pip`, `net-tools`, `python3-psutil`

**Optional Dependencies**: `snmp`, `avahi-utils` (for advanced features)

### Red Hat-based
- **Fedora** 35+
- **CentOS** 8+
- **RHEL** 8+ (Red Hat Enterprise Linux)
- **Rocky Linux** 8+
- **AlmaLinux** 8+

**Package Manager**: DNF/YUM

**Required Dependencies**: `nmap`, `iputils`, `python3`, `python3-pip`, `net-tools`, `python3-psutil`

**Optional Dependencies**: `net-snmp-utils`, `avahi-tools` (for advanced features)

**Note**: EPEL repository is automatically enabled for additional packages

### Arch-based
- **Arch Linux**
- **Manjaro**
- **EndeavourOS**

**Package Manager**: Pacman

**Required Dependencies**: `nmap`, `iputils`, `python`, `python-pip`, `net-tools`, `python-psutil`

**Optional Dependencies**: `net-snmp`, `avahi` (for advanced features)

### SUSE-based
- **openSUSE Leap** 15.3+
- **openSUSE Tumbleweed**
- **SLES** (SUSE Linux Enterprise Server) 15+

**Package Manager**: Zypper

**Required Dependencies**: `nmap`, `iputils`, `python3`, `python3-pip`, `net-tools`, `python3-psutil`

**Optional Dependencies**: `net-snmp`, `avahi-utils` (for advanced features)

## Installation

The installer automatically detects your distribution and uses the appropriate package manager:

```bash
# Download and run the installer
curl -sL https://raw.githubusercontent.com/username/ultimate-kea-dhcp-dashboard/main/install.sh -o install.sh
sudo bash install.sh
```

Or with the self-extracting installer:

```bash
# Download the installer
curl -sL https://raw.githubusercontent.com/username/ultimate-kea-dhcp-dashboard/main/ultimate-kea-dashboard-installer.sh -o installer.sh

# Run it
sudo bash installer.sh
```

## Distribution-Specific Configuration

### SSL Certificate Paths

Default SSL certificate paths vary by distribution:

| Distribution | Certificate | Key |
|--------------|-------------|-----|
| Debian/Ubuntu | `/etc/ssl/certs/ssl-cert-snakeoil.pem` | `/etc/ssl/private/ssl-cert-snakeoil.key` |
| Fedora/RHEL/CentOS | `/etc/pki/tls/certs/localhost.crt` | `/etc/pki/tls/private/localhost.key` |
| Arch/Manjaro | `/etc/ssl/certs/ssl-cert-snakeoil.pem` | `/etc/ssl/private/ssl-cert-snakeoil.key` |
| openSUSE | `/etc/ssl/certs/ssl-cert-snakeoil.pem` | `/etc/ssl/private/ssl-cert-snakeoil.key` |

The installer will prompt you with the correct default paths for your distribution.

### Kea DHCP Configuration Paths

Standard Kea configuration paths (same across distributions):
- Config: `/etc/kea/kea-dhcp4.conf`
- Leases: `/var/lib/kea/kea-leases4.csv`

### Systemd Service

All supported distributions use systemd for service management:

```bash
# Start service
sudo systemctl start ultimate-dashboard

# Enable on boot
sudo systemctl enable ultimate-dashboard

# Check status
sudo systemctl status ultimate-dashboard

# View logs
sudo journalctl -u ultimate-dashboard -f
```

## Firewall Configuration

### Debian/Ubuntu (UFW)
```bash
sudo ufw allow 8089/tcp
sudo ufw reload
```

### Fedora/RHEL/CentOS (firewalld)
```bash
sudo firewall-cmd --permanent --add-port=8089/tcp
sudo firewall-cmd --reload
```

### Arch/Manjaro (iptables or firewalld)
If using firewalld:
```bash
sudo firewall-cmd --permanent --add-port=8089/tcp
sudo firewall-cmd --reload
```

### openSUSE (firewalld)
```bash
sudo firewall-cmd --permanent --add-port=8089/tcp
sudo firewall-cmd --reload
```

## SELinux Considerations (RHEL/CentOS/Fedora)

If SELinux is enabled, you may need to configure it:

```bash
# Check SELinux status
sestatus

# Allow the dashboard port (if needed)
sudo semanage port -a -t http_port_t -p tcp 8089

# If you encounter permission issues
sudo ausearch -m avc -ts recent | grep ultimate-dashboard
```

For production deployments, create a custom SELinux policy instead of disabling SELinux.

## Package Manager Commands Reference

### Update System
```bash
# Debian/Ubuntu
sudo apt update && sudo apt upgrade

# Fedora/RHEL/CentOS
sudo dnf update

# Arch/Manjaro
sudo pacman -Syu

# openSUSE
sudo zypper update
```

### Install Dependencies Manually
```bash
# Debian/Ubuntu
sudo apt install nmap arping python3 python3-pip net-tools python3-psutil
# Optional: sudo apt install snmp avahi-utils

# Fedora/RHEL/CentOS
sudo dnf install nmap iputils python3 python3-pip net-tools python3-psutil
# Optional: sudo dnf install net-snmp-utils avahi-tools

# Arch/Manjaro
sudo pacman -S nmap iputils python python-pip net-tools python-psutil
# Optional: sudo pacman -S net-snmp avahi

# openSUSE
sudo zypper install nmap iputils python3 python3-pip net-tools python3-psutil
# Optional: sudo zypper install net-snmp avahi-utils
```

**Important**: psutil is installed via system package manager (not pip) to avoid conflicts and respect PEP 668.

## Troubleshooting

### Python Version
Ensure Python 3.8+ is installed:
```bash
python3 --version
```

### Missing Packages
If the automatic installation fails, install packages manually (see above).

### Permission Issues
The dashboard requires root privileges for network scanning:
```bash
sudo systemctl restart ultimate-dashboard
```

### Distribution Not Detected
If your distribution is not automatically detected, please open an issue at:
https://github.com/username/ultimate-kea-dashboard/issues

Include the output of:
```bash
cat /etc/os-release
```

## Contributing

To add support for additional distributions:
1. Test the installer on your distribution
2. Update the `detect_distro()` function in `install.sh`
3. Add distribution-specific configuration in `get_default_ssl_paths()`
4. Submit a pull request with your changes

## Support Matrix

| Distribution | Status | Notes |
|--------------|--------|-------|
| Debian 11+ | ✅ Tested | Full support |
| Ubuntu 20.04+ | ✅ Tested | Full support |
| Fedora 35+ | ✅ Tested | Full support |
| CentOS 8+ | ✅ Tested | Requires EPEL |
| Rocky Linux 8+ | ✅ Tested | Full support |
| AlmaLinux 8+ | ✅ Tested | Full support |
| Arch Linux | ✅ Tested | Full support |
| Manjaro | ⚠️ Community tested | Should work |
| openSUSE Leap | ⚠️ Community tested | Should work |
| openSUSE Tumbleweed | ⚠️ Community tested | Should work |

Legend:
- ✅ Tested: Officially tested and supported
- ⚠️ Community tested: Reported working by community
- ❌ Not supported: Known issues or unsupported

## Version Requirements

- Python: 3.8+
- Kea DHCP: 1.8+
- Systemd: Any recent version
- Linux Kernel: 4.15+
