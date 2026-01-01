"""
Custom device configuration and SVG icon generation
Allows users to define custom devices with personalized icons
"""

import json
from pathlib import Path

# Default config path
SCRIPT_DIR = Path(__file__).parent.parent.absolute()
CUSTOM_DEVICES_FILE = SCRIPT_DIR / 'etc' / 'custom-devices.json'

# In-memory cache
_custom_devices = []
_device_types = {}


def load_custom_devices(config_file=None):
    """
    Load custom device configurations from JSON file
    
    Args:
        config_file: Path to custom devices JSON (default: etc/custom-devices.json)
    
    Returns:
        tuple: (custom_devices list, device_types dict)
    """
    global _custom_devices, _device_types
    
    if config_file is None:
        config_file = CUSTOM_DEVICES_FILE
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _custom_devices = data.get('custom_devices', [])
            _device_types = data.get('device_types', {})
            print(f"[INFO] Loaded {len(_custom_devices)} custom devices from {config_file}")
            return _custom_devices, _device_types
    except FileNotFoundError:
        print(f"[WARN] Custom devices file not found: {config_file}")
        return [], {}
    except Exception as e:
        print(f"[ERROR] Failed to load custom devices: {e}")
        return [], {}


def get_custom_device(hostname):
    """
    Get custom device configuration by hostname
    
    Args:
        hostname: Device hostname
    
    Returns:
        dict or None: Custom device config if found
    """
    if not _custom_devices:
        load_custom_devices()
    
    h = hostname.lower() if hostname else ""
    for device in _custom_devices:
        if device.get('hostname', '').lower() in h:
            return device
    
    return None


def get_device_type_info(hostname, vendor=None, mac=None):
    """
    Get device type and label from custom configuration
    
    Args:
        hostname: Device hostname
        vendor: MAC vendor (optional)
        mac: MAC address (optional)
    
    Returns:
        tuple: (emoji, label, icon_name) or None
    """
    device = get_custom_device(hostname)
    if device:
        return (
            device.get('emoji', '❓'),
            device.get('label', 'Custom Device'),
            device.get('type', 'unknown')
        )
    
    return None


def generate_gaming_pc_svg(hostname, theme='master'):
    """
    Generate themed SVG icon for gaming PC
    
    Args:
        hostname: Device hostname
        theme: Icon theme (master, apprentice, etc.)
    
    Returns:
        str: SVG markup
    """
    h = hostname.lower() if hostname else ""
    
    # Marvin - Master Gaming PC (powerful setup with wide screen)
    if "marvin" in h or theme == "master":
        return """<svg width="24" height="24" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="marvin-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#ff4500;stop-opacity:1" />
                    <stop offset="50%" style="stop-color:#ffd700;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#ff4500;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="screen-glow" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#00ff88;stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:#0088ff;stop-opacity:0.8" />
                </linearGradient>
            </defs>
            <!-- Desk/Base -->
            <rect x="6" y="36" width="36" height="3" rx="1" fill="#333"/>
            <!-- Monitor stand -->
            <rect x="22" y="30" width="4" height="6" fill="#555"/>
            <rect x="18" y="35" width="12" height="2" rx="1" fill="#444"/>
            <!-- Large curved monitor -->
            <path d="M 8 12 Q 8 8 12 8 L 36 8 Q 40 8 40 12 L 40 28 Q 40 32 36 32 L 12 32 Q 8 32 8 28 Z" 
                  fill="#1a1a1a" stroke="url(#marvin-grad)" stroke-width="1.5"/>
            <!-- Screen glow -->
            <rect x="11" y="11" width="26" height="18" rx="1" fill="url(#screen-glow)" opacity="0.9"/>
            <!-- RGB lighting strips -->
            <rect x="6" y="38" width="8" height="1" fill="#ff0088" opacity="0.8"/>
            <rect x="18" y="38" width="12" height="1" fill="#00ff88" opacity="0.8"/>
            <rect x="34" y="38" width="8" height="1" fill="#0088ff" opacity="0.8"/>
            <!-- Power LED -->
            <circle cx="24" cy="34" r="1" fill="#00ff00" opacity="0.9">
                <animate attributeName="opacity" values="0.9;0.3;0.9" dur="2s" repeatCount="indefinite"/>
            </circle>
            <!-- Crown badge -->
            <path d="M 20 4 L 22 7 L 24 4 L 26 7 L 28 4 L 27 10 L 21 10 Z" fill="#ffd700" stroke="#ff4500" stroke-width="0.5"/>
            <text x="24" y="23" font-size="6" text-anchor="middle" fill="#ffd700" font-weight="bold" font-family="monospace">M</text>
        </svg>"""
    
    # Shepard - Apprentice Gaming PC (compact mini PC)
    elif "shepard" in h or theme == "apprentice":
        return """<svg width="24" height="24" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="shepard-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#4CAF50;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#2196F3;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="mini-screen" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#64B5F6;stop-opacity:0.9" />
                    <stop offset="100%" style="stop-color:#1976D2;stop-opacity:0.9" />
                </linearGradient>
            </defs>
            <!-- Desk -->
            <rect x="10" y="38" width="28" height="2" rx="1" fill="#444"/>
            <!-- Mini PC case (cube style) -->
            <rect x="14" y="20" width="12" height="14" rx="1" fill="#2a2a2a" stroke="url(#shepard-grad)" stroke-width="1.2"/>
            <!-- Front panel -->
            <rect x="15" y="22" width="10" height="11" fill="#1a1a1a"/>
            <!-- RGB fan (top) -->
            <circle cx="20" cy="25" r="3" fill="none" stroke="#4CAF50" stroke-width="0.8" opacity="0.7">
                <animateTransform attributeName="transform" type="rotate" from="0 20 25" to="360 20 25" dur="3s" repeatCount="indefinite"/>
            </circle>
            <!-- Power button -->
            <circle cx="20" cy="31" r="1.5" fill="#2196F3" opacity="0.8">
                <animate attributeName="opacity" values="0.8;0.4;0.8" dur="1.5s" repeatCount="indefinite"/>
            </circle>
            <!-- Small monitor -->
            <rect x="28" y="24" width="11" height="9" rx="0.5" fill="#1a1a1a" stroke="url(#shepard-grad)" stroke-width="1"/>
            <!-- Monitor screen -->
            <rect x="29" y="25" width="9" height="6" rx="0.3" fill="url(#mini-screen)"/>
            <!-- Monitor stand -->
            <rect x="32" y="33" width="3" height="4" fill="#555"/>
            <rect x="30" y="37" width="7" height="1" rx="0.5" fill="#444"/>
            <!-- Level indicator (learner badge) -->
            <rect x="15" y="40" width="4" height="1.5" fill="#4CAF50" opacity="0.8"/>
            <rect x="20" y="40" width="3" height="1.5" fill="#4CAF50" opacity="0.5"/>
            <rect x="24" y="40" width="2" height="1.5" fill="#666" opacity="0.3"/>
            <!-- Badge S -->
            <circle cx="20" cy="16" r="5" fill="url(#shepard-grad)" opacity="0.9"/>
            <text x="20" y="19" font-size="6" text-anchor="middle" fill="white" font-weight="bold" font-family="monospace">S</text>
        </svg>"""
    
    # Default generic gaming PC
    else:
        return """<svg width="24" height="24" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="pc-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#9C27B0;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#673AB7;stop-opacity:1" />
                </linearGradient>
            </defs>
            <!-- Desk -->
            <rect x="8" y="38" width="32" height="2" rx="1" fill="#444"/>
            <!-- Tower PC case -->
            <rect x="10" y="18" width="10" height="18" rx="1" fill="#2a2a2a" stroke="url(#pc-grad)" stroke-width="1.2"/>
            <rect x="11" y="20" width="8" height="15" fill="#1a1a1a"/>
            <!-- RGB fans -->
            <circle cx="15" cy="24" r="2.5" fill="none" stroke="#9C27B0" stroke-width="0.7" opacity="0.7">
                <animateTransform attributeName="transform" type="rotate" from="0 15 24" to="360 15 24" dur="2s" repeatCount="indefinite"/>
            </circle>
            <circle cx="15" cy="30" r="2.5" fill="none" stroke="#673AB7" stroke-width="0.7" opacity="0.7">
                <animateTransform attributeName="transform" type="rotate" from="360 15 30" to="0 15 30" dur="2s" repeatCount="indefinite"/>
            </circle>
            <!-- Monitor -->
            <rect x="24" y="20" width="14" height="12" rx="0.5" fill="#1a1a1a" stroke="url(#pc-grad)" stroke-width="1"/>
            <rect x="25" y="21" width="12" height="9" rx="0.3" fill="#673AB7" opacity="0.3"/>
            <!-- Monitor stand -->
            <rect x="29" y="32" width="4" height="5" fill="#555"/>
            <rect x="27" y="37" width="8" height="1" rx="0.5" fill="#444"/>
            <!-- Power LED -->
            <circle cx="15" cy="35" r="1" fill="#9C27B0" opacity="0.9">
                <animate attributeName="opacity" values="0.9;0.4;0.9" dur="1.5s" repeatCount="indefinite"/>
            </circle>
        </svg>"""


def get_custom_icon_svg(hostname):
    """
    Get custom SVG icon for device based on hostname
    
    Args:
        hostname: Device hostname
    
    Returns:
        str or None: SVG markup if custom icon exists
    """
    if not hostname:
        return None
    
    device = get_custom_device(hostname)
    if device and device.get('type') == 'gaming-pc':
        theme = device.get('icon_theme', 'generic')
        return generate_gaming_pc_svg(hostname, theme)
    
    return None


# Auto-load on module import
load_custom_devices()
