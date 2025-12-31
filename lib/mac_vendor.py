"""MAC address vendor lookup utilities"""
import json
import urllib.request
import time
from pathlib import Path


MAC_VENDOR_CACHE = {}
MAC_VENDOR_DB = None


def load_mac_vendor_db(oui_file='/opt/ultimate-dashboard/data/oui.json'):
    """Load MAC vendor database from local OUI JSON file"""
    global MAC_VENDOR_DB
    
    if MAC_VENDOR_DB is not None:
        return MAC_VENDOR_DB
    
    try:
        if Path(oui_file).exists():
            with open(oui_file, 'r') as f:
                MAC_VENDOR_DB = json.load(f)
            print(f"[INFO] Loaded {len(MAC_VENDOR_DB)} MAC vendors from local database")
        else:
            print(f"[WARN] OUI database not found at {oui_file}")
            MAC_VENDOR_DB = {}
    except Exception as e:
        print(f"[ERROR] Failed to load OUI database: {e}")
        MAC_VENDOR_DB = {}
    
    return MAC_VENDOR_DB


def get_mac_vendor(mac, enable_api_fallback=True, timeout=2):
    """Get MAC vendor from local OUI database with optional API fallback"""
    if not mac:
        return "N/A"
    
    mac_clean = mac.upper().replace('-', ':')
    mac_prefix = ':'.join(mac_clean.split(':')[:3])
    
    if mac_prefix in MAC_VENDOR_CACHE:
        return MAC_VENDOR_CACHE[mac_prefix]
    
    db = load_mac_vendor_db()
    if mac_prefix in db:
        vendor = db[mac_prefix]
        if len(vendor) > 30:
            vendor = vendor.split(',')[0].split('(')[0].strip()
        MAC_VENDOR_CACHE[mac_prefix] = vendor
        return vendor
    
    if enable_api_fallback:
        try:
            url = f"https://api.macvendors.com/{mac_prefix}"
            response = urllib.request.urlopen(url, timeout=timeout)
            vendor = response.read().decode().strip()
            if len(vendor) > 30:
                vendor = vendor.split(',')[0].split('(')[0].strip()
            MAC_VENDOR_CACHE[mac_prefix] = vendor
            time.sleep(0.5)
            return vendor
        except Exception:
            pass
    
    MAC_VENDOR_CACHE[mac_prefix] = "Unknown"
    return "Unknown"
