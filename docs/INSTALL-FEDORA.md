# Fedora Installation

> **Languages / Langues:** 🇬🇧 [English](INSTALL-FEDORA.md) | 🇫🇷 [Français](INSTALL-FEDORA.fr.md)

---

Specific installation guide for Fedora, RHEL, CentOS, Rocky Linux, and AlmaLinux.

## Quick Installation

```bash
# Download the installer
curl -sL https://raw.githubusercontent.com/username/ultimate-kea-dhcp-dashboard/main/install.sh -o install.sh

# Run (automatically detects Fedora/RHEL and uses DNF/YUM)
sudo bash install.sh
```

For complete French documentation, see [INSTALL-FEDORA.fr.md](INSTALL-FEDORA.fr.md).

## Key Points for Fedora/RHEL

- **Package Manager**: DNF (Fedora, RHEL 8+) or YUM (older systems)
- **EPEL**: Automatically enabled for RHEL/CentOS/Rocky/AlmaLinux
- **Firewall**: firewalld (configure port 8089)
- **SELinux**: Enabled by default (configure contexts)
- **SSL Paths**: `/etc/pki/tls/certs/` and `/etc/pki/tls/private/`

## Essential Commands

```bash
# Install dependencies
sudo dnf install -y nmap iputils python3 python3-pip net-tools python3-psutil net-snmp-utils avahi-tools

# Configure firewall
sudo firewall-cmd --permanent --add-port=8089/tcp
sudo firewall-cmd --reload

# Configure SELinux
sudo semanage port -a -t http_port_t -p tcp 8089

# Manage service
sudo systemctl enable --now ultimate-dashboard
sudo systemctl status ultimate-dashboard
sudo journalctl -u ultimate-dashboard -f
```

## See Also

- [Complete French Guide](INSTALL-FEDORA.fr.md) - Detailed Fedora/RHEL installation
- [Supported Distributions](DISTRIBUTIONS.md) - All supported distributions
- [Dependencies](DEPENDENCIES.md) - Dependency details

---

**For full documentation in French, see [INSTALL-FEDORA.fr.md](INSTALL-FEDORA.fr.md)**
