# Installation Guide

## Prerequisites

Before installing Ultimate Kea Dashboard, ensure you have:

1. **Operating System**
   - Debian 10+ or Ubuntu 20.04+ (or compatible distribution)
   - Root or sudo access

2. **Kea DHCP Server**
   - Kea DHCP installed and configured
   - MySQL/MariaDB backend enabled
   - Database credentials available

3. **Network Access**
   - Access to the network you want to monitor
   - Firewall rules allowing dashboard port (default: 8089)

## Quick Installation

The easiest way to install:

```bash
curl -fsSL https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/releases/latest/download/quick-install.sh | sudo bash
```

## Manual Installation

### Step 1: Download

```bash
# Download the latest release
wget https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/releases/latest/download/ultimate-kea-dashboard-v1.0.0.tar.gz

# Extract
tar -xzf ultimate-kea-dashboard-v1.0.0.tar.gz
cd installer
```

### Step 2: Run Installer

```bash
sudo ./install.sh
```

### Step 3: Follow the Interactive Wizard

The installer will guide you through:

1. **Welcome Screen**
   - Overview of the installation process

2. **Dependency Check**
   - Automatic installation of required packages
   - Python libraries installation

3. **Kea Database Configuration**
   - Database host (default: localhost)
   - Database port (default: 3306)
   - Database name (default: kea)
   - Database user (default: kea)
   - Database password

4. **Network Configuration**
   - DHCP pool start IP
   - DHCP pool end IP
   - Subnet (CIDR notation)
   - Reserved IP ranges (comma-separated)

5. **Dashboard Settings**
   - Dashboard port (default: 8089)
   - Refresh interval in seconds (default: 30)
   - Auto-scan on startup (default: yes)
   - SNMP community (default: public, optional)

6. **Installation**
   - Files copied to `/opt/ultimate-dashboard`
   - Service configured and started
   - Auto-start enabled

7. **Completion**
   - Access URL displayed
   - Service status shown

## Post-Installation

### Access the Dashboard

Open your browser and navigate to:
```
http://YOUR_SERVER_IP:8089
```

### Verify Service Status

```bash
sudo systemctl status ultimate-dashboard
```

### View Logs

```bash
# Real-time logs
sudo journalctl -u ultimate-dashboard -f

# Recent logs
sudo journalctl -u ultimate-dashboard -n 100
```

### Manage the Service

```bash
# Start
sudo systemctl start ultimate-dashboard

# Stop
sudo systemctl stop ultimate-dashboard

# Restart
sudo systemctl restart ultimate-dashboard

# Disable auto-start
sudo systemctl disable ultimate-dashboard

# Enable auto-start
sudo systemctl enable ultimate-dashboard
```

## Configuration

### Edit Configuration

```bash
sudo nano /opt/ultimate-dashboard/etc/config.ini
```

After editing, restart the service:
```bash
sudo systemctl restart ultimate-dashboard
```

### Configuration Sections

**[kea]**
- Database connection settings

**[network]**
- DHCP pool and subnet configuration

**[dashboard]**
- Dashboard behavior settings

**[snmp]**
- SNMP community for device queries

## Troubleshooting

### Dashboard Won't Start

1. Check logs: `sudo journalctl -u ultimate-dashboard -n 50`
2. Verify config: `cat /opt/ultimate-dashboard/etc/config.ini`
3. Test database connection: `mysql -h HOST -u USER -p DATABASE`

### Can't Connect to Dashboard

1. Check if service is running: `sudo systemctl status ultimate-dashboard`
2. Verify port is listening: `sudo netstat -tlnp | grep 8089`
3. Check firewall: `sudo ufw status` or `sudo iptables -L`

### No DHCP Leases Shown

1. Verify Kea is using MySQL backend
2. Check database credentials in config
3. Ensure Kea database has active leases

### Scanning Not Working

1. Verify network configuration in config.ini
2. Check system has necessary tools (nmap, arp, snmpwalk)
3. Ensure proper network access

## Uninstallation

To completely remove the dashboard:

```bash
sudo /opt/ultimate-dashboard/bin/uninstall.sh
```

This will:
- Stop and disable the service
- Remove all installed files
- Remove the systemd service
- Optionally remove dependencies

## Upgrading

When a new version is released:

```bash
# Download new version
wget https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/releases/latest/download/ultimate-kea-dashboard-vX.X.X.tar.gz

# Stop current service
sudo systemctl stop ultimate-dashboard

# Backup configuration
sudo cp /opt/ultimate-dashboard/etc/config.ini /tmp/config.ini.backup

# Extract and run installer
tar -xzf ultimate-kea-dashboard-vX.X.X.tar.gz
cd installer
sudo ./install.sh

# Restore configuration if needed
sudo cp /tmp/config.ini.backup /opt/ultimate-dashboard/etc/config.ini

# Restart service
sudo systemctl restart ultimate-dashboard
```

## Support

Need help? 
- Check [Troubleshooting](#troubleshooting) above
- Read the [FAQ](https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/wiki/FAQ)
- Open an [Issue](https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/issues)
- Join [Discussions](https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/discussions)
