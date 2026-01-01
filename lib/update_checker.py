"""Update checker for Ultimate Kea Dashboard"""
import urllib.request
import json
import subprocess
from pathlib import Path

def get_current_version():
    """Get current installed version"""
    version_file = Path('/opt/ultimate-kea-dashboard/VERSION')
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

if __name__ == '__main__':
    result = check_for_updates()
    print(json.dumps(result))
