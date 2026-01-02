#!/bin/bash
set -e

VERSION=$(cat ../VERSION)
PACKAGE_NAME="ultimate-kea-dashboard"
BUILD_DIR="/tmp/${PACKAGE_NAME}-build"
DEB_DIR="${BUILD_DIR}/${PACKAGE_NAME}_${VERSION}"

# Clean and create build directory
rm -rf "$BUILD_DIR"
mkdir -p "$DEB_DIR"

# Create DEBIAN directory
mkdir -p "$DEB_DIR/DEBIAN"

# Copy control file
cp debian/control "$DEB_DIR/DEBIAN/"
sed -i "s/VERSION/${VERSION}/g" "$DEB_DIR/DEBIAN/control"

# Copy postinst and prerm scripts if they exist
[ -f debian/postinst ] && cp debian/postinst "$DEB_DIR/DEBIAN/" && chmod 755 "$DEB_DIR/DEBIAN/postinst"
[ -f debian/prerm ] && cp debian/prerm "$DEB_DIR/DEBIAN/" && chmod 755 "$DEB_DIR/DEBIAN/prerm"

# Create installation directories
mkdir -p "$DEB_DIR/opt/ultimate-kea-dashboard"
mkdir -p "$DEB_DIR/etc/systemd/system"

# Copy application files
cd ..
cp -r bin lib static etc *.py *.sh requirements.txt VERSION "$DEB_DIR/opt/ultimate-kea-dashboard/"

# Copy systemd service
cp etc/ultimate-kea-dashboard.service "$DEB_DIR/etc/systemd/system/"

# Build the package
cd "$BUILD_DIR"
dpkg-deb --build "${PACKAGE_NAME}_${VERSION}"

# Move to current directory
mv "${PACKAGE_NAME}_${VERSION}.deb" "$OLDPWD/"

echo "Package built: ${PACKAGE_NAME}_${VERSION}.deb"
