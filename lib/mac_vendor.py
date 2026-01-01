"""MAC address vendor lookup utilities"""
import json
import urllib.request
import time
import os
from pathlib import Path
from datetime import datetime, timedelta


MAC_VENDOR_CACHE = {}
MAC_VENDOR_DB = None
OUI_UPDATE_INTERVAL = timedelta(days=30)  # Update OUI database every 30 days


def download_oui_database(oui_file='/opt/ultimate-kea-dashboard/data/oui.json'):
    """Download and update OUI database from IEEE"""
    print(f"[INFO] Downloading OUI database...")
    
    try:
        # Download from IEEE OUI database
        url = "https://standards-oui.ieee.org/oui/oui.txt"
        response = urllib.request.urlopen(url, timeout=60)
        oui_txt = response.read().decode('utf-8', errors='ignore')
        
        # Parse OUI data
        oui_db = {}
        for line in oui_txt.split('\n'):
            if '(hex)' in line:
                parts = line.split('(hex)')
                if len(parts) == 2:
                    mac_prefix = parts[0].strip().replace('-', ':')
                    vendor = parts[1].strip()
                    oui_db[mac_prefix] = vendor
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(oui_file), exist_ok=True)
        
        # Save to file
        with open(oui_file, 'w') as f:
            json.dump(oui_db, f, indent=2)
        
        print(f"[INFO] Downloaded {len(oui_db)} MAC vendors to {oui_file}")
        return oui_db
        
    except Exception as e:
        print(f"[ERROR] Failed to download OUI database: {e}")
        return {}


def check_and_update_oui_db(oui_file='/opt/ultimate-kea-dashboard/data/oui.json'):
    """Check if OUI database needs updating and update if necessary"""
    oui_path = Path(oui_file)
    
    # Check if file exists and its age
    needs_update = False
    
    if not oui_path.exists():
        print(f"[INFO] OUI database not found, downloading...")
        needs_update = True
    else:
        # Check file age
        file_mtime = datetime.fromtimestamp(oui_path.stat().st_mtime)
        if datetime.now() - file_mtime > OUI_UPDATE_INTERVAL:
            print(f"[INFO] OUI database is older than {OUI_UPDATE_INTERVAL.days} days, updating...")
            needs_update = True
    
    if needs_update:
        return download_oui_database(oui_file)
    
    return None


def load_mac_vendor_db(oui_file='/opt/ultimate-kea-dashboard/data/oui.json'):
    """Load MAC vendor database from local OUI JSON file"""
    global MAC_VENDOR_DB
    
    if MAC_VENDOR_DB is not None:
        return MAC_VENDOR_DB
    
    # Check and update database if needed
    updated_db = check_and_update_oui_db(oui_file)
    if updated_db:
        MAC_VENDOR_DB = updated_db
        return MAC_VENDOR_DB
    
    # Load existing database
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
