#!/bin/bash
# Script to create self-extracting installer

OUTPUT="ultimate-kea-dashboard-installer.sh"

cat > "$OUTPUT" << 'HEADER'
#!/bin/bash
#
# Ultimate Kea DHCP Dashboard - Self-Extracting Installer
# https://github.com/username/ultimate-kea-dashboard
#
# This is a self-contained installer that extracts and installs the dashboard.
# Usage: bash ultimate-kea-dashboard-installer.sh
#

set -e

INSTALL_DIR="/opt/ukd"
TEMP_DIR=$(mktemp -d)

echo "=================================================="
echo "  Ultimate Kea DHCP Dashboard Installer v1.0.0"
echo "=================================================="
echo ""

cleanup() {
    echo "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

echo "Extracting files to $TEMP_DIR..."

# Find the line number where the archive starts
ARCHIVE_LINE=$(awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' "$0")

# Extract the archive
tail -n+$ARCHIVE_LINE "$0" | base64 -d | tar xzf - -C "$TEMP_DIR"

echo "Running installer..."
cd "$TEMP_DIR"
bash install.sh

echo ""
echo "Installation complete!"
echo "Access the dashboard at: http://$(hostname -I | awk '{print $1}'):8089"
echo ""

exit 0

__ARCHIVE_BELOW__
HEADER

# Create tar archive of all files except .git
tar czf - --exclude='.git' --exclude='create-installer.sh' --exclude='ultimate-kea-dashboard-installer.sh' . | base64 >> "$OUTPUT"

chmod +x "$OUTPUT"

echo "Self-extracting installer created: $OUTPUT"
ls -lh "$OUTPUT"
