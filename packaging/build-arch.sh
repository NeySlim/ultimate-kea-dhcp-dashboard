#!/bin/bash
set -e

# Determine project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

VERSION=$(cat "$PROJECT_ROOT/VERSION")
PACKAGE_NAME="ultimate-kea-dashboard"
BUILD_DIR="/tmp/${PACKAGE_NAME}-arch-build"
PKG_DIR="${BUILD_DIR}/pkg"
SRC_DIR="${BUILD_DIR}/src/${PACKAGE_NAME}-${VERSION}"

# Clean and create build directories
rm -rf "$BUILD_DIR"
mkdir -p "$PKG_DIR" "$SRC_DIR"

# Copy project files to source directory
cd "$PROJECT_ROOT"
for dir in bin lib static etc data; do
    [ -d "$dir" ] && cp -r "$dir" "$SRC_DIR/"
done
for file in requirements.txt VERSION start.sh; do
    [ -f "$file" ] && cp "$file" "$SRC_DIR/" 2>/dev/null || true
done

# Copy PKGBUILD and update version
cp "$SCRIPT_DIR/arch/PKGBUILD" "$BUILD_DIR/"
cd "$BUILD_DIR"
sed -i "s/pkgver=.*/pkgver=${VERSION}/" PKGBUILD

# Create package structure manually
mkdir -p "${PKG_DIR}/opt/ultimate-kea-dashboard"
mkdir -p "${PKG_DIR}/etc/ultimate-kea-dashboard"
mkdir -p "${PKG_DIR}/var/log/ultimate-kea-dashboard"
mkdir -p "${PKG_DIR}/usr/lib/systemd/system"

# Copy application files
cp -r "$SRC_DIR"/* "${PKG_DIR}/opt/ultimate-kea-dashboard/"

# Copy systemd service
cp "$SRC_DIR/etc/ultimate-kea-dashboard.service" "${PKG_DIR}/usr/lib/systemd/system/"

# Create .PKGINFO
cat > "${PKG_DIR}/.PKGINFO" <<EOF
pkgname = ${PACKAGE_NAME}
pkgver = ${VERSION}-1
pkgdesc = Modern web dashboard for Kea DHCP Server
url = https://github.com/neyser/ultimate-kea-dashboard
builddate = $(date +%s)
packager = NeySlim <neyslim@example.com>
size = $(du -sb "${PKG_DIR}" | cut -f1)
arch = any
license = MIT
depend = kea>=2.0.0
depend = python>=3.8
depend = python-pip
depend = net-snmp
depend = nmap
depend = net-tools
depend = iproute2
depend = curl
depend = sqlite
optdepend = kea-ctrl-agent: For enhanced Kea integration
backup = etc/ultimate-kea-dashboard/config.json
EOF

# Create .MTREE
cd "$PKG_DIR"
bsdtar -czf .MTREE --format=mtree \
    --options='!all,use-set,type,uid,gid,mode,time,size,md5,sha256,link' \
    .PKGINFO *

# Create the package
cd "$BUILD_DIR"
env LANG=C bsdtar -cf - -C "$PKG_DIR" .MTREE .PKGINFO * | zstd -19 > "${PACKAGE_NAME}-${VERSION}-1-any.pkg.tar.zst"

# Move to packaging directory
mv "${PACKAGE_NAME}-${VERSION}-1-any.pkg.tar.zst" "$SCRIPT_DIR/"

echo "Arch package built successfully: ${PACKAGE_NAME}-${VERSION}-1-any.pkg.tar.zst"
