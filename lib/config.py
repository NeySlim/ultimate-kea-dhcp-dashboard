"""
Configuration module for Ultimate Kea Dashboard
Handles configuration loading and global settings
"""

import configparser
import threading
from pathlib import Path

# Script directory
SCRIPT_DIR = Path(__file__).parent.parent.absolute()

# Configuration file paths (checked in order)
CONFIG_PATHS = [
    str(SCRIPT_DIR / 'etc' / 'ultimate-dashboard.conf'),
    '/etc/ultimate-dashboard/ultimate-dashboard.conf',
    './ultimate-dashboard.conf',
    '/opt/ultimate-dashboard/etc/ultimate-dashboard.conf',
]

# Default configuration
DEFAULT_CONFIG = {
    'port': 8089,
    'use_ssl': False,
    'cert_file': '/path/to/your/cert.crt',
    'key_file': '/path/to/your/key.key',
    'leases_file': '/var/lib/kea/kea-leases4.csv',
    'kea_socket': '/run/kea/kea4-ctrl-socket',
    'bind_address': '',
    'enable_mac_vendor': True,
    'mac_vendor_timeout': 2,
    'reverse_dns_timeout': 2,
    'enable_snmp': True,
    'snmp_communities': ['public'],
    'snmp_timeout': 1,
    'enable_mdns': True,
    'mdns_timeout': 1,
    'enable_scanner': True,
    'scanner_timeout': 5
}

# Global configuration (singleton)
config = DEFAULT_CONFIG.copy()

# Global caches and locks
DEVICE_INFO_CACHE = {}
NETWORK_SCAN_RESULTS = {}
STATIC_DEVICE_ENHANCED_DATA = {}
LAST_SCAN_TIME = {}
SCAN_IN_PROGRESS = {}
CACHE_LOCK = threading.Lock()
SCAN_THREAD = None


def load_config():
    """
    Load configuration from file
    
    Tries each path in CONFIG_PATHS until one is found.
    Falls back to default configuration if no file is found.
    
    Returns:
        dict: Configuration dictionary
    """
    global config
    
    config_parser = configparser.ConfigParser()
    config_file = None
    
    # Try each config path
    for path in CONFIG_PATHS:
        try:
            if config_parser.read(path):
                config_file = path
                print(f"[INFO] Loaded configuration from: {path}")
                break
        except Exception as e:
            print(f"[WARNING] Could not read config from {path}: {e}")
            continue
    
    if not config_file:
        print("[WARNING] No configuration file found, using defaults")
        return config
    
    # Parse configuration
    try:
        if config_parser.has_section('DEFAULT'):
            section = config_parser['DEFAULT']
            
            # Server settings
            config['port'] = section.getint('port', fallback=config['port'])
            config['bind_address'] = section.get('bind_address', fallback=config['bind_address'])
            config['use_ssl'] = section.getboolean('ssl_enabled', fallback=config['use_ssl'])
            config['cert_file'] = section.get('ssl_cert', fallback=config['cert_file'])
            config['key_file'] = section.get('ssl_key', fallback=config['key_file'])
            
            # Kea settings
            config['kea_socket'] = section.get('kea_socket', fallback=config['kea_socket'])
            config['leases_file'] = section.get('kea_leases', fallback=config['leases_file'])
            
            # Feature toggles
            config['enable_scanner'] = section.getboolean('enable_scanner', fallback=config['enable_scanner'])
            config['enable_mac_vendor'] = section.getboolean('enable_mac_vendor', fallback=config['enable_mac_vendor'])
            config['enable_snmp'] = section.getboolean('enable_snmp', fallback=config['enable_snmp'])
            config['enable_mdns'] = section.getboolean('enable_mdns', fallback=config['enable_mdns'])
            
            # Timeouts
            config['scanner_timeout'] = section.getint('scan_timeout', fallback=config['scanner_timeout'])
            config['mac_vendor_timeout'] = section.getint('mac_vendor_timeout', fallback=config['mac_vendor_timeout'])
            config['reverse_dns_timeout'] = section.getint('reverse_dns_timeout', fallback=config['reverse_dns_timeout'])
            config['snmp_timeout'] = section.getint('snmp_timeout', fallback=config['snmp_timeout'])
            
            # Parse SNMP communities (comma-separated list)
            communities_str = section.get('snmp_communities', fallback=None)
            if not communities_str:
                communities_str = section.get('snmp_community', fallback='public')
            config['snmp_communities'] = [c.strip() for c in communities_str.split(',')]
            
            config['mdns_timeout'] = section.getint('mdns_timeout', fallback=config['mdns_timeout'])
            
            print("[INFO] Configuration loaded successfully")
    except Exception as e:
        print(f"[ERROR] Error parsing configuration: {e}")
        print("[WARNING] Using default configuration")
    
    return config


def get_config(key=None, default=None):
    """
    Get configuration value
    
    Args:
        key: Configuration key (None to get all config)
        default: Default value if key not found
    
    Returns:
        Configuration value or dict
    """
    if key is None:
        return config
    return config.get(key, default)


def set_config(key, value):
    """
    Set configuration value (runtime only, not persisted)
    
    Args:
        key: Configuration key
        value: Configuration value
    """
    global config
    config[key] = value


def reload_config():
    """Reload configuration from file"""
    return load_config()
