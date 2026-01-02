#!/bin/bash
set -e

VERSION=$(cat ../VERSION)
PACKAGE_NAME="ultimate-kea-dashboard"
BUILD_DIR="/tmp/${PACKAGE_NAME}-arch-build"

# Clean and create build directory
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Copy PKGBUILD
cp arch/PKGBUILD "$BUILD_DIR/"
cd "$BUILD_DIR"

# Update version in PKGBUILD
sed -i "s/pkgver=.*/pkgver=${VERSION}/" PKGBUILD

# Build package
makepkg -sf --noconfirm

# Move package to packaging directory
mv *.pkg.tar.* "$OLDPWD/"

echo "Arch package built successfully"
