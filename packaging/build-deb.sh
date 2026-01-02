#!/bin/bash
set -e

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

VERSION=$(cat "$PROJECT_ROOT/VERSION")
PACKAGE_NAME="ultimate-kea-dashboard"
BUILD_DIR="/tmp/${PACKAGE_NAME}-build"
DEB_DIR="${BUILD_DIR}/${PACKAGE_NAME}_${VERSION}"

# Clean and create build directory
rm -rf "$BUILD_DIR"
mkdir -p "$DEB_DIR"

# Create DEBIAN directory
mkdir -p "$DEB_DIR/DEBIAN"

# Copy control file
cp "$SCRIPT_DIR/debian/control.binary" "$DEB_DIR/DEBIAN/control"
sed -i "s/VERSION/${VERSION}/g" "$DEB_DIR/DEBIAN/control"

# Copy postinst and prerm scripts if they exist
[ -f "$SCRIPT_DIR/debian/postinst" ] && cp "$SCRIPT_DIR/debian/postinst" "$DEB_DIR/DEBIAN/" && chmod 755 "$DEB_DIR/DEBIAN/postinst"
[ -f "$SCRIPT_DIR/debian/prerm" ] && cp "$SCRIPT_DIR/debian/prerm" "$DEB_DIR/DEBIAN/" && chmod 755 "$DEB_DIR/DEBIAN/prerm"

# Create installation directories
mkdir -p "$DEB_DIR/opt/ultimate-kea-dashboard"
mkdir -p "$DEB_DIR/etc/systemd/system"

# Copy application files from project root
cd "$PROJECT_ROOT"
for dir in bin lib static data etc; do
    [ -d "$dir" ] && cp -r "$dir" "$DEB_DIR/opt/ultimate-kea-dashboard/"
done
for file in requirements.txt VERSION *.sh; do
    [ -f "$file" ] && cp "$file" "$DEB_DIR/opt/ultimate-kea-dashboard/" 2>/dev/null || true
done

# Copy systemd service
cp "$PROJECT_ROOT/etc/ultimate-kea-dashboard.service" "$DEB_DIR/etc/systemd/system/"

# Build the package
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"

# Move to packaging directory
mv "${PACKAGE_NAME}_${VERSION}.deb" "$SCRIPT_DIR/"

echo "Package built: $SCRIPT_DIR/${PACKAGE_NAME}_${VERSION}.deb"
