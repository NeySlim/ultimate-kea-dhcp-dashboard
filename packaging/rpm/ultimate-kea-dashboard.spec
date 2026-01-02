Name:           ultimate-kea-dashboard
Version:        @VERSION@
Release:        1%{?dist}
Summary:        Modern web dashboard for Kea DHCP Server

License:        MIT
URL:            https://github.com/neyser/ultimate-kea-dashboard
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       kea-dhcp4 >= 2.0.0
Requires:       python3 >= 3.8
Requires:       python3-pip
Requires:       net-snmp-utils
Requires:       nmap
Requires:       net-tools
Requires:       iproute
Requires:       curl
Requires:       sqlite

%description
Ultimate Kea Dashboard is a modern, responsive web-based dashboard
for monitoring and managing ISC Kea DHCP servers.

Features include:
- Real-time DHCP lease monitoring
- Network device scanning with SNMP support
- Service discovery (SSH, HTTP, HTTPS)
- MAC address vendor identification
- Multi-subnet support
- Automatic updates
- Customizable themes
- Multi-language support (EN/FR)

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf $RPM_BUILD_ROOT

# Create directories
mkdir -p $RPM_BUILD_ROOT/opt/ultimate-kea-dashboard
mkdir -p $RPM_BUILD_ROOT/etc/ultimate-kea-dashboard
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system
mkdir -p $RPM_BUILD_ROOT/var/log/ultimate-kea-dashboard

# Copy application files
cp -r bin lib static $RPM_BUILD_ROOT/opt/ultimate-kea-dashboard/
mkdir -p $RPM_BUILD_ROOT/opt/ultimate-kea-dashboard/data
if [ -d data ]; then
    cp -r data/* $RPM_BUILD_ROOT/opt/ultimate-kea-dashboard/data/ 2>/dev/null || true
fi
for file in start.sh requirements.txt; do
    [ -f "$file" ] && cp "$file" $RPM_BUILD_ROOT/opt/ultimate-kea-dashboard/
done
[ -f VERSION ] && cp VERSION $RPM_BUILD_ROOT/opt/ultimate-kea-dashboard/

# Copy configuration
cp -r etc/* $RPM_BUILD_ROOT/etc/ultimate-kea-dashboard/

# Install systemd service
cp etc/ultimate-kea-dashboard.service $RPM_BUILD_ROOT/usr/lib/systemd/system/

%pre
# Create user if doesn't exist
if ! id ultimate-kea-dashboard >/dev/null 2>&1; then
    useradd --system --home-dir /opt/ultimate-kea-dashboard --no-create-home \
            --shell /sbin/nologin ultimate-kea-dashboard
fi

%post
# Create directories if they don't exist
mkdir -p /opt/ultimate-kea-dashboard || true
mkdir -p /opt/ultimate-kea-dashboard/data || true
mkdir -p /etc/ultimate-kea-dashboard || true
mkdir -p /var/log/ultimate-kea-dashboard || true

# Set permissions only if directories exist
[ -d /opt/ultimate-kea-dashboard ] && chown -R ultimate-kea-dashboard:ultimate-kea-dashboard /opt/ultimate-kea-dashboard || true
[ -d /etc/ultimate-kea-dashboard ] && chown -R ultimate-kea-dashboard:ultimate-kea-dashboard /etc/ultimate-kea-dashboard || true
[ -d /var/log/ultimate-kea-dashboard ] && chown -R ultimate-kea-dashboard:ultimate-kea-dashboard /var/log/ultimate-kea-dashboard || true

# Install Python dependencies
if [ -f /opt/ultimate-kea-dashboard/requirements.txt ]; then
    cd /opt/ultimate-kea-dashboard
    pip3 install -r requirements.txt >/dev/null 2>&1 || true
fi

# Download OUI database if not present
if [ -d /opt/ultimate-kea-dashboard/data ] && [ ! -f /opt/ultimate-kea-dashboard/data/oui.txt ]; then
    curl -s -o /opt/ultimate-kea-dashboard/data/oui.txt \
         http://standards-oui.ieee.org/oui/oui.txt || true
fi

# Reload systemd
systemctl daemon-reload

# Enable and start service
systemctl enable ultimate-kea-dashboard.service
systemctl start ultimate-kea-dashboard.service

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Ultimate Kea Dashboard installed successfully!             ║"
echo "║                                                              ║"
echo "║  Access at: http://your-server:8089                         ║"
echo "║                                                              ║"
echo "║  Service commands:                                           ║"
echo "║    systemctl status ultimate-kea-dashboard                  ║"
echo "║    systemctl restart ultimate-kea-dashboard                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

%preun
if [ $1 -eq 0 ]; then
    # Uninstall
    systemctl stop ultimate-kea-dashboard.service || true
    systemctl disable ultimate-kea-dashboard.service || true
fi

%postun
if [ $1 -eq 0 ]; then
    # Purge
    if id ultimate-kea-dashboard >/dev/null 2>&1; then
        userdel ultimate-kea-dashboard || true
    fi
    rm -rf /var/log/ultimate-kea-dashboard
fi

%files
%defattr(-,root,root,-)
%attr(0755,ultimate-kea-dashboard,ultimate-kea-dashboard) /opt/ultimate-kea-dashboard
/opt/ultimate-kea-dashboard/bin
/opt/ultimate-kea-dashboard/lib
/opt/ultimate-kea-dashboard/static
/opt/ultimate-kea-dashboard/data
%attr(0755,root,root) /opt/ultimate-kea-dashboard/start.sh
/opt/ultimate-kea-dashboard/requirements.txt
/opt/ultimate-kea-dashboard/VERSION
%config(noreplace) /etc/ultimate-kea-dashboard
/usr/lib/systemd/system/ultimate-kea-dashboard.service
%dir %attr(0755,ultimate-kea-dashboard,ultimate-kea-dashboard) /var/log/ultimate-kea-dashboard

%changelog
* Thu Jan 02 2025 NeySlim <neyslim@example.com> - 1.6.1-1
- New upstream release 1.6.1
- Added native packaging for Debian/Ubuntu, Red Hat/Fedora, and Arch Linux
- Automated package building via GitHub Actions
- All packages include Kea DHCP server as dependency
- Automatic service and user setup

* Thu Jan 02 2025 NeySlim <neyslim@example.com> - 1.5.6-1
- New upstream release 1.5.6
- Added configurable refresh interval
- Improved vendor lookup with OUI database
- Enhanced SNMP details display with hover tooltips
- Fixed static devices table sorting
- Added automatic update checker
- Improved ARP filtering for static devices
- Added service discovery count with details on hover
- Multiple bug fixes and performance improvements
