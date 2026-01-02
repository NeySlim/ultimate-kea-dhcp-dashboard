#!/bin/bash
set -e

VERSION=$(cat ../VERSION)
PACKAGE_NAME="ultimate-kea-dashboard"
BUILD_DIR="/tmp/${PACKAGE_NAME}-rpm-build"
SPEC_FILE="rpm/${PACKAGE_NAME}.spec"

# Clean and create build directories
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Create source tarball
cd ..
tar czf "$BUILD_DIR/SOURCES/${PACKAGE_NAME}-${VERSION}.tar.gz" \
    --transform "s,^,${PACKAGE_NAME}-${VERSION}/," \
    bin lib static etc *.py *.sh requirements.txt VERSION

# Copy and update spec file
cd packaging
cp "$SPEC_FILE" "$BUILD_DIR/SPECS/"
sed -i "s/VERSION/${VERSION}/g" "$BUILD_DIR/SPECS/${PACKAGE_NAME}.spec"

# Build RPM
rpmbuild --define "_topdir $BUILD_DIR" \
         -ba "$BUILD_DIR/SPECS/${PACKAGE_NAME}.spec"

# Move RPM to current directory
mv "$BUILD_DIR/RPMS"/*/*.rpm ./ 2>/dev/null || true
mv "$BUILD_DIR/SRPMS"/*.rpm ./ 2>/dev/null || true

echo "RPM package(s) built successfully"
