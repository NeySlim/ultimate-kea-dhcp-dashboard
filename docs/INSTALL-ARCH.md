# Arch Linux Installation

> **Languages / Langues:** 🇬🇧 [English](INSTALL-ARCH.md) | 🇫🇷 [Français](INSTALL-ARCH.fr.md)

---

Specific installation guide for Arch Linux, Manjaro, and EndeavourOS.

## Quick Installation

```bash
# Download the installer
curl -sL https://raw.githubusercontent.com/username/ultimate-kea-dhcp-dashboard/main/install.sh -o install.sh

# Run (automatically detects Arch and uses Pacman)
sudo bash install.sh
```

For complete French documentation, see [INSTALL-ARCH.fr.md](INSTALL-ARCH.fr.md).

## Key Points for Arch Linux

- **Package Manager**: Pacman
- **Python**: `python` (not `python3`)
- **Firewall**: nftables (recommended) or firewalld/iptables
- **Philosophy**: Everything via pacman (avoid pip for system packages)
- **Avahi**: Daemon must be started manually

## Essential Commands

```bash
# Update system
sudo pacman -Syu

# Install dependencies
sudo pacman -S nmap iputils python python-pip net-tools python-psutil net-snmp avahi

# Enable Avahi daemon
sudo systemctl enable --now avahi-daemon

# Manage service
sudo systemctl enable --now ultimate-dashboard
sudo systemctl status ultimate-dashboard
sudo journalctl -u ultimate-dashboard -f
```

## Firewall Configuration (nftables)

```bash
# Edit configuration
sudo nano /etc/nftables.conf
```

Add:
```
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        iif lo accept
        ct state established,related accept
        tcp dport 22 accept
        tcp dport 8089 accept
    }
}
```

Enable:
```bash
sudo systemctl enable --now nftables
```

## See Also

- [Complete French Guide](INSTALL-ARCH.fr.md) - Detailed Arch Linux installation
- [Supported Distributions](DISTRIBUTIONS.md) - All supported distributions
- [Dependencies](DEPENDENCIES.md) - Dependency details
- [Arch Wiki](https://wiki.archlinux.org/) - General Arch documentation

---

**For full documentation in French, see [INSTALL-ARCH.fr.md](INSTALL-ARCH.fr.md)**
