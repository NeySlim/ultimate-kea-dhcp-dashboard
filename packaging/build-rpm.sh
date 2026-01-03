#!/bin/bash
set -e

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

FULL_VERSION=$(cat "$PROJECT_ROOT/VERSION")
# RPM requires Version and Release to be separate
# Split version like "1.6.9-1" into VERSION=1.6.9 and RELEASE=1
if [[ "$FULL_VERSION" == *-* ]]; then
    VERSION="${FULL_VERSION%-*}"
    RELEASE="${FULL_VERSION##*-}"
else
    VERSION="$FULL_VERSION"
    RELEASE="1"
fi
PACKAGE_NAME="ultimate-kea-dashboard"
BUILD_DIR="/tmp/${PACKAGE_NAME}-rpm-build"
SPEC_FILE="$SCRIPT_DIR/rpm/${PACKAGE_NAME}.spec"

# Clean and create build directories
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Create source tarball
cd "$PROJECT_ROOT"
tar czf "$BUILD_DIR/SOURCES/${PACKAGE_NAME}-${VERSION}.tar.gz" \
    --transform "s,^,${PACKAGE_NAME}-${VERSION}/," \
    --exclude='.git*' --exclude='packaging' --exclude='*.md' \
    --exclude='logs' --exclude='*.pyc' --exclude='__pycache__' \
    .

# Copy and update spec file
cp "$SPEC_FILE" "$BUILD_DIR/SPECS/"
sed -i "s/@VERSION@/${VERSION}/g" "$BUILD_DIR/SPECS/${PACKAGE_NAME}.spec"
sed -i "s/@RELEASE@/${RELEASE}/g" "$BUILD_DIR/SPECS/${PACKAGE_NAME}.spec"

# Build RPM
rpmbuild --define "_topdir $BUILD_DIR" \
         -ba "$BUILD_DIR/SPECS/${PACKAGE_NAME}.spec"

# Move RPM to packaging directory
mv "$BUILD_DIR/RPMS"/*/*.rpm "$SCRIPT_DIR/" 2>/dev/null || true
mv "$BUILD_DIR/SRPMS"/*.rpm "$SCRIPT_DIR/" 2>/dev/null || true

echo "RPM package(s) built successfully"
