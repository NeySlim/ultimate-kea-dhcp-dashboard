#!/bin/bash

# Ultimate Kea DHCP Dashboard - Installer
# Interactive installer with Blossom theme aesthetics

set -e

# Colors and styling for Blossom theme
PINK='\033[38;5;218m'
DARK='\033[38;5;234m'
ACCENT='\033[38;5;176m'
GREEN='\033[38;5;150m'
CYAN='\033[38;5;117m'
RESET='\033[0m'
BOLD='\033[1m'

# Box drawing characters
BOX_TL="╔"
BOX_TR="╗"
BOX_BL="╚"
BOX_BR="╝"
BOX_H="═"
BOX_V="║"

# Installation directories
INSTALL_DIR="/opt/ultimate-dashboard"
BIN_DIR="$INSTALL_DIR/bin"
ETC_DIR="$INSTALL_DIR/etc"
LIB_DIR="$INSTALL_DIR/lib"
DATA_DIR="$INSTALL_DIR/data"
LOGS_DIR="$INSTALL_DIR/logs"
STATIC_DIR="$INSTALL_DIR/static"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
DEFAULT_PORT=8089
DEFAULT_SSL=false
DEFAULT_CERT="/root/pinet.crt"
DEFAULT_KEY="/root/pinet.key"
DEFAULT_LEASES="/var/lib/kea/kea-leases4.csv"
DEFAULT_SOCKET="/run/kea/kea4-ctrl-socket"
DEFAULT_BIND=""
DEFAULT_MAC_VENDOR=true
DEFAULT_MAC_TIMEOUT=2
DEFAULT_DNS_TIMEOUT=2
DEFAULT_SNMP=true
DEFAULT_SNMP_COMMUNITY="home"
DEFAULT_SNMP_TIMEOUT=1
DEFAULT_MDNS=true
DEFAULT_MDNS_TIMEOUT=1
DEFAULT_SCANNER=true
DEFAULT_SUBNET="192.168.1.0/24"
DEFAULT_SCANNER_TIMEOUT=5

# Function to draw a box
draw_box() {
    local width=$1
    local text=$2
    local padding=$(( (width - ${#text} - 2) / 2 ))
    
    echo -ne "${PINK}${BOX_TL}"
    printf "${BOX_H}%.0s" $(seq 1 $width)
    echo -e "${BOX_TR}${RESET}"
    
    if [ -n "$text" ]; then
        echo -ne "${PINK}${BOX_V}${RESET}"
        printf "%${padding}s" ""
        echo -ne "${BOLD}${ACCENT}${text}${RESET}"
        printf "%$(( width - padding - ${#text} ))s" ""
        echo -e "${PINK}${BOX_V}${RESET}"
    fi
}

# Function to close box
close_box() {
    local width=$1
    echo -ne "${PINK}${BOX_BL}"
    printf "${BOX_H}%.0s" $(seq 1 $width)
    echo -e "${BOX_BR}${RESET}"
}

# Function to print centered text
print_centered() {
    local text=$1
    local width=70
    local padding=$(( (width - ${#text}) / 2 ))
    
    printf "%${padding}s" ""
    echo -e "${BOLD}${text}${RESET}"
}

# Function to print section header
print_section() {
    local text=$1
    echo ""
    echo -e "${PINK}${BOX_H}${BOX_H}${BOX_H}${RESET} ${BOLD}${CYAN}${text}${RESET}"
    echo ""
}

# Function to prompt for input with default
prompt_input() {
    local prompt=$1
    local default=$2
    local var_name=$3
    local is_password=${4:-false}
    
    if [ "$is_password" = true ]; then
        echo -ne "${ACCENT}${prompt}${RESET} ${DARK}[${default}]${RESET}: "
        read -s input_value
        echo ""
    else
        echo -ne "${ACCENT}${prompt}${RESET} ${DARK}[${default}]${RESET}: "
        read input_value
    fi
    
    if [ -z "$input_value" ]; then
        eval "$var_name='$default'"
    else
        eval "$var_name='$input_value'"
    fi
}

# Function to prompt for yes/no
prompt_yesno() {
    local prompt=$1
    local default=$2
    local var_name=$3
    
    if [ "$default" = true ]; then
        default_text="Y/n"
    else
        default_text="y/N"
    fi
    
    echo -ne "${ACCENT}${prompt}${RESET} ${DARK}[${default_text}]${RESET}: "
    read answer
    
    if [ -z "$answer" ]; then
        eval "$var_name='$default'"
    elif [[ "$answer" =~ ^[Yy] ]]; then
        eval "$var_name=true"
    else
        eval "$var_name=false"
    fi
}

# Function to show spinner
spinner() {
    local pid=$1
    local msg=$2
    local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    local i=0
    
    echo -ne "${CYAN}${msg}${RESET} "
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) %10 ))
        echo -ne "\r${CYAN}${msg}${RESET} ${PINK}${spin:$i:1}${RESET}"
        sleep 0.1
    done
    echo -ne "\r${CYAN}${msg}${RESET} ${GREEN}✓${RESET}\n"
}

# Clear screen and show banner
clear
echo ""
draw_box 70 ""
echo -ne "${PINK}${BOX_V}${RESET}"
printf "%70s" ""
echo -e "${PINK}${BOX_V}${RESET}"

print_centered "${PINK}🌸 Ultimate Kea DHCP Dashboard 🌸${RESET}"

echo -ne "${PINK}${BOX_V}${RESET}"
printf "%70s" ""
echo -e "${PINK}${BOX_V}${RESET}"

echo -ne "${PINK}${BOX_V}${RESET}"
printf "%20s" ""
echo -ne "${ACCENT}Blossom Theme Edition${RESET}"
printf "%29s" ""
echo -e "${PINK}${BOX_V}${RESET}"

echo -ne "${PINK}${BOX_V}${RESET}"
printf "%70s" ""
echo -e "${PINK}${BOX_V}${RESET}"
close_box 70
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${PINK}❌ Please run as root${RESET}"
    exit 1
fi

echo -e "${GREEN}Welcome to the Ultimate Dashboard installer!${RESET}"
echo ""
echo "This installer will guide you through the installation process."
echo "You can press Enter to accept default values."
echo ""

# Server Configuration
print_section "🖥️  Server Configuration"

prompt_input "Port to listen on" "$DEFAULT_PORT" "PORT"
prompt_yesno "Enable HTTPS" "$DEFAULT_SSL" "USE_SSL"

if [ "$USE_SSL" = true ]; then
    prompt_input "Certificate file path" "$DEFAULT_CERT" "CERT_FILE"
    prompt_input "Key file path" "$DEFAULT_KEY" "KEY_FILE"
else
    CERT_FILE="$DEFAULT_CERT"
    KEY_FILE="$DEFAULT_KEY"
fi

prompt_input "Bind address (leave empty for all interfaces)" "$DEFAULT_BIND" "BIND_ADDR"

# Kea Configuration
print_section "🔑 Kea DHCP Configuration"

prompt_input "Path to Kea leases CSV file" "$DEFAULT_LEASES" "LEASES_FILE"
prompt_input "Path to Kea control socket" "$DEFAULT_SOCKET" "KEA_SOCKET"

# Network Scanner Configuration
print_section "🌐 Network Scanner Configuration"

prompt_yesno "Enable network scanner" "$DEFAULT_SCANNER" "ENABLE_SCANNER"
if [ "$ENABLE_SCANNER" = true ]; then
    prompt_input "Subnet to scan (CIDR notation)" "$DEFAULT_SUBNET" "SCANNER_SUBNET"
    prompt_input "Scanner timeout (seconds)" "$DEFAULT_SCANNER_TIMEOUT" "SCANNER_TIMEOUT"
else
    SCANNER_SUBNET="$DEFAULT_SUBNET"
    SCANNER_TIMEOUT="$DEFAULT_SCANNER_TIMEOUT"
fi

# MAC Vendor Lookup
print_section "🏷️  MAC Vendor Lookup"

prompt_yesno "Enable MAC vendor lookup" "$DEFAULT_MAC_VENDOR" "ENABLE_MAC_VENDOR"
if [ "$ENABLE_MAC_VENDOR" = true ]; then
    prompt_input "MAC vendor timeout (seconds)" "$DEFAULT_MAC_TIMEOUT" "MAC_TIMEOUT"
else
    MAC_TIMEOUT="$DEFAULT_MAC_TIMEOUT"
fi

# DNS Configuration
print_section "🌍 DNS Configuration"

prompt_input "Reverse DNS timeout (seconds)" "$DEFAULT_DNS_TIMEOUT" "DNS_TIMEOUT"

# SNMP Configuration
print_section "📡 SNMP Configuration"

prompt_yesno "Enable SNMP" "$DEFAULT_SNMP" "ENABLE_SNMP"
if [ "$ENABLE_SNMP" = true ]; then
    prompt_input "SNMP community string" "$DEFAULT_SNMP_COMMUNITY" "SNMP_COMMUNITY"
    prompt_input "SNMP timeout (seconds)" "$DEFAULT_SNMP_TIMEOUT" "SNMP_TIMEOUT"
else
    SNMP_COMMUNITY="$DEFAULT_SNMP_COMMUNITY"
    SNMP_TIMEOUT="$DEFAULT_SNMP_TIMEOUT"
fi

# mDNS Configuration
print_section "📻 mDNS Configuration"

prompt_yesno "Enable mDNS" "$DEFAULT_MDNS" "ENABLE_MDNS"
if [ "$ENABLE_MDNS" = true ]; then
    prompt_input "mDNS timeout (seconds)" "$DEFAULT_MDNS_TIMEOUT" "MDNS_TIMEOUT"
else
    MDNS_TIMEOUT="$DEFAULT_MDNS_TIMEOUT"
fi

# Installation confirmation
echo ""
print_section "📦 Installation Summary"
echo ""
echo -e "Installation directory: ${CYAN}${INSTALL_DIR}${RESET}"
echo -e "Port: ${CYAN}${PORT}${RESET}"
echo -e "HTTPS: ${CYAN}${USE_SSL}${RESET}"
echo -e "Kea leases: ${CYAN}${LEASES_FILE}${RESET}"
echo -e "Network scanner: ${CYAN}${ENABLE_SCANNER}${RESET}"
echo ""

prompt_yesno "Proceed with installation?" true "PROCEED"

if [ "$PROCEED" != true ]; then
    echo -e "${PINK}Installation cancelled.${RESET}"
    exit 0
fi

# Create directories
print_section "📁 Creating directories"
(mkdir -p "$BIN_DIR" "$ETC_DIR" "$LIB_DIR" "$DATA_DIR" "$LOGS_DIR" "$STATIC_DIR") &
spinner $! "Creating directory structure"

# Install system dependencies
print_section "📦 Installing system dependencies"

echo -ne "${CYAN}Updating package list...${RESET} "
apt-get update > /dev/null 2>&1 &
spinner $! "Updating package list"

DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    nmap \
    net-tools \
    iproute2 \
    iputils-ping \
    dnsutils \
    snmp \
    snmp-mibs-downloader \
    avahi-utils \
    tcpdump \
    libpcap-dev \
    build-essential > /dev/null 2>&1 &
spinner $! "Installing system packages"

# Copy source files
print_section "📋 Copying files"

SOURCE_DIR="$SCRIPT_DIR/ultimate-dashboard"

if [ -d "$SOURCE_DIR/bin" ]; then
    (cp -r "$SOURCE_DIR/bin/"* "$BIN_DIR/") &
    spinner $! "Copying binaries"
fi

if [ -d "$SOURCE_DIR/lib" ]; then
    (cp -r "$SOURCE_DIR/lib/"* "$LIB_DIR/") &
    spinner $! "Copying libraries"
fi

if [ -d "$SOURCE_DIR/static" ]; then
    (cp -r "$SOURCE_DIR/static/"* "$STATIC_DIR/") &
    spinner $! "Copying static files"
fi

if [ -f "$SOURCE_DIR/start.sh" ]; then
    (cp "$SOURCE_DIR/start.sh" "$INSTALL_DIR/") &
    spinner $! "Copying startup script"
    chmod +x "$INSTALL_DIR/start.sh"
fi

if [ -f "$SOURCE_DIR/README.md" ]; then
    (cp "$SOURCE_DIR/README.md" "$INSTALL_DIR/") &
    spinner $! "Copying documentation"
fi

# Set proper permissions
chmod +x "$BIN_DIR/"* 2>/dev/null || true

# Create configuration file
print_section "⚙️  Creating configuration"

cat > "$ETC_DIR/ultimate-dashboard.conf" << EOF
[server]
# Port to listen on
port = $PORT

# Enable HTTPS (true/false)
use_ssl = $USE_SSL

# Certificate file path
cert_file = $CERT_FILE

# Key file path  
key_file = $KEY_FILE

# Path to Kea leases CSV file
leases_file = $LEASES_FILE

# Path to Kea control socket
kea_socket = $KEA_SOCKET

# Bind address (empty for 0.0.0.0)
bind_address = $BIND_ADDR

# Enable MAC vendor lookup (true/false)
enable_mac_vendor = $ENABLE_MAC_VENDOR

# MAC vendor API timeout in seconds
mac_vendor_timeout = $MAC_TIMEOUT

# Reverse DNS lookup timeout in seconds
reverse_dns_timeout = $DNS_TIMEOUT

# SNMP settings
enable_snmp = $ENABLE_SNMP
snmp_community = $SNMP_COMMUNITY
snmp_timeout = $SNMP_TIMEOUT

# mDNS settings
enable_mdns = $ENABLE_MDNS
mdns_timeout = $MDNS_TIMEOUT

# Network scanner settings
enable_scanner = $ENABLE_SCANNER
scanner_subnet = $SCANNER_SUBNET
scanner_timeout = $SCANNER_TIMEOUT
EOF

echo -e "${GREEN}✓${RESET} Configuration file created"

# Create custom devices file if doesn't exist
if [ ! -f "$ETC_DIR/custom-devices.txt" ]; then
    touch "$ETC_DIR/custom-devices.txt"
    echo -e "${GREEN}✓${RESET} Custom devices file created"
fi

# Create systemd service
print_section "🚀 Creating systemd service"

cat > /etc/systemd/system/ultimate-dashboard.service << EOF
[Unit]
Description=Ultimate Kea DHCP Dashboard
After=network.target kea-dhcp4.service

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $BIN_DIR/ultimate-dashboard
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

(systemctl daemon-reload) &
spinner $! "Reloading systemd"

# Install Python dependencies
print_section "🐍 Installing Python dependencies"

pip3 install --upgrade pip > /dev/null 2>&1 &
spinner $! "Upgrading pip"

pip3 install \
    flask \
    waitress \
    pysnmp \
    pysnmp-mibs \
    requests \
    netifaces \
    psutil \
    scapy > /dev/null 2>&1 &
spinner $! "Installing Python packages"

# Enable and start service
print_section "✨ Finalizing installation"

(systemctl enable ultimate-dashboard.service) &
spinner $! "Enabling service"

(systemctl start ultimate-dashboard.service) &
spinner $! "Starting service"

# Show completion message
echo ""
draw_box 70 ""
echo -ne "${PINK}${BOX_V}${RESET}"
printf "%70s" ""
echo -e "${PINK}${BOX_V}${RESET}"

print_centered "${GREEN}🎉 Installation Complete! 🎉${RESET}"

echo -ne "${PINK}${BOX_V}${RESET}"
printf "%70s" ""
echo -e "${PINK}${BOX_V}${RESET}"
close_box 70
echo ""

echo -e "${CYAN}Dashboard is now running on:${RESET}"
if [ "$USE_SSL" = true ]; then
    echo -e "  ${BOLD}https://$(hostname):${PORT}${RESET}"
else
    echo -e "  ${BOLD}http://$(hostname):${PORT}${RESET}"
fi
echo ""
echo -e "${ACCENT}Useful commands:${RESET}"
echo -e "  ${CYAN}systemctl status ultimate-dashboard${RESET}  - Check service status"
echo -e "  ${CYAN}systemctl restart ultimate-dashboard${RESET} - Restart service"
echo -e "  ${CYAN}journalctl -u ultimate-dashboard -f${RESET}  - View logs"
echo ""
echo -e "${PINK}Configuration file: ${CYAN}$ETC_DIR/ultimate-dashboard.conf${RESET}"
echo ""
echo -e "${GREEN}Enjoy your dashboard! 🌸${RESET}"
echo ""
