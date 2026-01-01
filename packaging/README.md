# Distribution Packages

This directory contains packaging files for multiple Linux distributions.

## Supported Distributions

### Debian/Ubuntu (.deb)
- **Location:** `debian/`
- **Supported versions:** Debian 11+, Ubuntu 20.04+
- **Dependencies:** Automatically handles Kea DHCP, Python 3.8+, and all required tools

### Red Hat/Fedora/CentOS (.rpm)
- **Location:** `rpm/`
- **Supported versions:** Fedora 35+, RHEL 8+, Rocky Linux 8+
- **Dependencies:** Kea DHCP 2.0+, Python 3.8+

### Arch Linux (.pkg.tar.zst)
- **Location:** `arch/`
- **Supported versions:** Current Arch Linux
- **Dependencies:** Managed via pacman

## Installation

### Debian/Ubuntu
```bash
sudo dpkg -i ultimate-kea-dashboard_*.deb
sudo apt-get install -f  # Install dependencies if needed
```

### Red Hat/Fedora/CentOS
```bash
sudo dnf install ultimate-kea-dashboard-*.rpm
# or
sudo rpm -i ultimate-kea-dashboard-*.rpm
```

### Arch Linux
```bash
sudo pacman -U ultimate-kea-dashboard-*.pkg.tar.zst
```

## Building Manually

### Debian/Ubuntu
```bash
cd /path/to/ultimate-kea-dashboard
VERSION=$(cat VERSION)
mkdir -p ../ultimate-kea-dashboard-${VERSION}
cp -r * ../ultimate-kea-dashboard-${VERSION}/
cp -r packaging/debian ../ultimate-kea-dashboard-${VERSION}/
cd ../ultimate-kea-dashboard-${VERSION}
dpkg-buildpackage -us -uc -b
```

### Red Hat/Fedora
```bash
rpmdev-setuptree
VERSION=$(cat VERSION)
tar czf ~/rpmbuild/SOURCES/ultimate-kea-dashboard-${VERSION}.tar.gz .
cp packaging/rpm/ultimate-kea-dashboard.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild/SPECS
rpmbuild -bb ultimate-kea-dashboard.spec
```

### Arch Linux
```bash
VERSION=$(cat VERSION)
tar czf ultimate-kea-dashboard-${VERSION}.tar.gz .
cp packaging/arch/PKGBUILD .
cp packaging/arch/ultimate-kea-dashboard.install .
makepkg -s
```

## Automatic Builds

All packages are automatically built via GitHub Actions on every release tag.
Download pre-built packages from the [Releases](https://github.com/neyser/ultimate-kea-dashboard/releases) page.
