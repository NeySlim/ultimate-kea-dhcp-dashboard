"""Update checker for Ultimate Kea Dashboard"""
import urllib.request
import json
import subprocess
from pathlib import Path

def get_current_version():
    """Get current installed version"""
    version_file = Path('/opt/ukd/VERSION')
    if version_file.exists():
        return version_file.read_text().strip()
    return "unknown"

def get_latest_version():
    """Get latest version from GitHub releases"""
    try:
        url = "https://api.github.com/repos/NeySlim/ultimate-kea-dhcp-dashboard/releases/latest"
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Ultimate-Kea-Dashboard-Checker')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get('tag_name', '').lstrip('v')
    except Exception as e:
        print(f"[ERROR] Failed to check for updates: {e}")
        return None

def compare_versions(current, latest):
    """Compare version strings"""
    if not latest or latest == "unknown":
        return 0
    
    try:
        current_parts = [int(x) for x in current.split('.')]
        latest_parts = [int(x) for x in latest.split('.')]
        
        for c, l in zip(current_parts, latest_parts):
            if l > c:
                return 1  # Update available
            elif l < c:
                return -1  # Current is newer
        
        # Check if latest has more parts
        if len(latest_parts) > len(current_parts):
            return 1
        
        return 0  # Same version
    except:
        return 0

def check_for_updates():
    """Check if update is available"""
    current = get_current_version()
    latest = get_latest_version()
    
    return {
        'current_version': current,
        'latest_version': latest or "unknown",
        'update_available': compare_versions(current, latest) > 0,
        'error': latest is None
    }

def detect_install_method():
    """Detect how the dashboard was installed"""
    install_dir = Path('/opt/ukd')
    
    # Check for git installation
    if (install_dir / '.git').exists():
        return 'git'
    
    # Check for package manager markers
    if Path('/var/lib/dpkg/info/ultimate-kea-dashboard.list').exists():
        return 'deb'
    
    if Path('/var/lib/rpm').exists():
        # Check if RPM package is installed
        try:
            result = subprocess.run(
                ['rpm', '-q', 'ultimate-kea-dashboard'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'rpm'
        except:
            pass
    
    # Check for Arch package
    if Path('/var/lib/pacman/local').exists():
        try:
            result = subprocess.run(
                ['pacman', '-Q', 'ultimate-kea-dashboard'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'arch'
        except:
            pass
    
    return 'unknown'

def update_via_git(install_dir):
    """Update via git pull"""
    # Stash any local changes before pulling
    stash_result = subprocess.run(
        ['git', 'stash', 'push', '-u', '-m', 'Auto-stash before update'],
        cwd=str(install_dir),
        capture_output=True,
        text=True,
        timeout=10
    )
    
    # Perform git pull
    result = subprocess.run(
        ['git', 'pull'],
        cwd=str(install_dir),
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        return {
            'success': False,
            'error': True,
            'message': f'Git pull failed: {result.stderr}'
        }
    
    # Try to reapply stashed changes (optional, ignore if it fails)
    if 'No local changes to save' not in stash_result.stdout:
        subprocess.run(
            ['git', 'stash', 'pop'],
            cwd=str(install_dir),
            capture_output=True,
            text=True,
            timeout=10
        )
    
    return {'success': True, 'error': False}

def update_via_package(package_type):
    """Update via package manager"""
    latest_version = get_latest_version()
    if not latest_version:
        return {
            'success': False,
            'error': True,
            'message': 'Could not fetch latest version from GitHub'
        }
    
    # Download package
    base_url = f"https://github.com/NeySlim/ultimate-kea-dhcp-dashboard/releases/download/v{latest_version}"
    
    if package_type == 'deb':
        package_file = f"/tmp/ultimate-kea-dashboard_{latest_version}.deb"
        package_url = f"{base_url}/ultimate-kea-dashboard_{latest_version}.deb"
        install_cmd = ['apt-get', 'install', '-y', package_file]
    elif package_type == 'rpm':
        package_file = f"/tmp/ultimate-kea-dashboard-{latest_version}-1.el9.x86_64.rpm"
        package_url = f"{base_url}/ultimate-kea-dashboard-{latest_version}-1.el9.x86_64.rpm"
        install_cmd = ['dnf', 'install', '-y', package_file]
    elif package_type == 'arch':
        package_file = f"/tmp/ultimate-kea-dashboard-{latest_version}-1-x86_64.pkg.tar.zst"
        package_url = f"{base_url}/ultimate-kea-dashboard-{latest_version}-1-x86_64.pkg.tar.zst"
        install_cmd = ['pacman', '-U', '--noconfirm', package_file]
    else:
        return {
            'success': False,
            'error': True,
            'message': f'Unsupported package type: {package_type}'
        }
    
    try:
        # Download package
        req = urllib.request.Request(package_url)
        req.add_header('User-Agent', 'Ultimate-Kea-Dashboard-Updater')
        
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(package_file, 'wb') as f:
                f.write(response.read())
        
        # Install package
        result = subprocess.run(
            install_cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Clean up downloaded package
        Path(package_file).unlink(missing_ok=True)
        
        if result.returncode != 0:
            return {
                'success': False,
                'error': True,
                'message': f'Package installation failed: {result.stderr}'
            }
        
        return {'success': True, 'error': False}
        
    except Exception as e:
        # Clean up on error
        Path(package_file).unlink(missing_ok=True)
        return {
            'success': False,
            'error': True,
            'message': f'Package download/install failed: {str(e)}'
        }

def perform_update():
    """Perform the dashboard update"""
    try:
        install_dir = Path('/opt/ukd')
        install_method = detect_install_method()
        
        # Perform update based on installation method
        if install_method == 'git':
            result = update_via_git(install_dir)
        elif install_method in ['deb', 'rpm', 'arch']:
            result = update_via_package(install_method)
        else:
            return {
                'success': False,
                'error': True,
                'message': 'Could not detect installation method. Manual update required.'
            }
        
        if not result.get('success'):
            return result
        
        # Restart service (common for all methods)
        restart_result = subprocess.run(
            ['systemctl', 'restart', 'ultimate-kea-dashboard'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if restart_result.returncode != 0:
            return {
                'success': False,
                'error': True,
                'message': f'Service restart failed: {restart_result.stderr}'
            }
        
        return {
            'success': True,
            'error': False,
            'message': 'Update completed successfully. Dashboard is restarting...'
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': True,
            'message': 'Update timeout. Please try manually.'
        }
    except Exception as e:
        return {
            'success': False,
            'error': True,
            'message': f'Update failed: {str(e)}'
        }

if __name__ == '__main__':
    result = check_for_updates()
    print(json.dumps(result))
