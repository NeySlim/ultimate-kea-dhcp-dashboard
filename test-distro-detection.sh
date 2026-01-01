#!/bin/bash
###############################################################################
# Distribution Detection Test Script
# Tests the multi-distribution detection system
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Distribution Detection Test${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    DISTRO_VERSION=$VERSION_ID
    DISTRO_NAME=$NAME
elif [ -f /etc/redhat-release ]; then
    DISTRO="rhel"
    DISTRO_NAME="Red Hat Enterprise Linux"
elif [ -f /etc/debian_version ]; then
    DISTRO="debian"
    DISTRO_NAME="Debian"
else
    DISTRO="unknown"
    DISTRO_NAME="Unknown"
fi

# Determine package manager
case "$DISTRO" in
    debian|ubuntu|linuxmint|pop)
        PKG_MANAGER="apt"
        ;;
    fedora)
        PKG_MANAGER="dnf"
        ;;
    centos|rhel|rocky|almalinux)
        if command -v dnf &> /dev/null; then
            PKG_MANAGER="dnf"
        else
            PKG_MANAGER="yum"
        fi
        ;;
    arch|manjaro|endeavouros)
        PKG_MANAGER="pacman"
        ;;
    opensuse*|sles)
        PKG_MANAGER="zypper"
        ;;
    *)
        PKG_MANAGER="unknown"
        ;;
esac

echo -e "${YELLOW}Detected System Information:${NC}"
echo -e "  Distribution ID:    ${GREEN}${DISTRO}${NC}"
echo -e "  Distribution Name:  ${GREEN}${DISTRO_NAME}${NC}"
echo -e "  Version:            ${GREEN}${DISTRO_VERSION:-N/A}${NC}"
echo -e "  Package Manager:    ${GREEN}${PKG_MANAGER}${NC}"
echo ""

# Test if package manager is supported
if [[ "$PKG_MANAGER" == "unknown" ]]; then
    echo -e "${RED}✗ Unsupported distribution!${NC}"
    echo -e "  This distribution is not yet supported by the installer."
    echo -e "  Please open an issue on GitHub with your distribution information."
    exit 1
else
    echo -e "${GREEN}✓ Distribution is supported!${NC}"
fi

# Check if package manager exists
if command -v ${PKG_MANAGER} &> /dev/null; then
    echo -e "${GREEN}✓ Package manager '${PKG_MANAGER}' is available${NC}"
else
    echo -e "${RED}✗ Package manager '${PKG_MANAGER}' not found!${NC}"
    exit 1
fi

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python 3 found (version ${PYTHON_VERSION})${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
fi

# Check if systemd is available
if command -v systemctl &> /dev/null; then
    echo -e "${GREEN}✓ Systemd is available${NC}"
else
    echo -e "${YELLOW}⚠ Systemd not found - service management may not work${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Test completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"

