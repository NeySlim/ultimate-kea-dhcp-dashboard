#!/bin/bash
set -e

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

VERSION=$(cat "$PROJECT_ROOT/VERSION")
PACKAGE_NAME="ultimate-kea-dashboard"
BUILD_DIR="/tmp/${PACKAGE_NAME}-arch-build"

# Clean and create build directory
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Copy PKGBUILD
cp "$SCRIPT_DIR/arch/PKGBUILD" "$BUILD_DIR/"
cd "$BUILD_DIR"

# Update version in PKGBUILD
sed -i "s/pkgver=.*/pkgver=${VERSION}/" PKGBUILD

# Build package
makepkg -sf --noconfirm

# Move package to packaging directory
mv *.pkg.tar.* "$SCRIPT_DIR/"

echo "Arch package built successfully"
