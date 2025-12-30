#!/bin/bash
# Quick installer script for Ultimate Kea Dashboard
# This downloads and runs the full interactive installer

set -e

echo "=================================="
echo "Ultimate Kea DHCP Dashboard"
echo "Quick Installer"
echo "=================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root or with sudo"
    exit 1
fi

# Download the full installer
INSTALL_SCRIPT_URL="https://github.com/YOUR_USERNAME/ultimate-kea-dashboard/releases/latest/download/install.sh"

echo "📥 Downloading installer..."
if command -v wget &> /dev/null; then
    wget -q --show-progress -O /tmp/ukd-install.sh "$INSTALL_SCRIPT_URL"
elif command -v curl &> /dev/null; then
    curl -fsSL -o /tmp/ukd-install.sh "$INSTALL_SCRIPT_URL"
else
    echo "❌ Neither wget nor curl is installed. Please install one of them."
    exit 1
fi

chmod +x /tmp/ukd-install.sh

echo "🚀 Starting installation..."
echo ""

/tmp/ukd-install.sh "$@"

# Cleanup
rm -f /tmp/ukd-install.sh

echo ""
echo "✅ Installation complete!"
