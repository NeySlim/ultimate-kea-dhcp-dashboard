"""
Utility functions for Ultimate Kea Dashboard
Common helpers for hostname resolution, datetime formatting, etc.
"""

import socket
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def resolve_hostname(ip):
    """
    Try to resolve hostname from IP via reverse DNS
    
    Args:
        ip: IP address
    
    Returns:
        Hostname or None
    """
    try:
        result = socket.gethostbyaddr(ip)
        if result and result[0]:
            return result[0]
    except:
        pass
    return None


def get_mdns_info(hostname, timeout=1):
    """
    Get mDNS info for hostname using Avahi
    
    Args:
        hostname: Hostname to lookup
        timeout: Timeout in seconds
    
    Returns:
        mDNS information string or None
    """
    if not hostname or hostname == "N/A":
        return None
    
    try:
        # Try to resolve via mDNS
        result = subprocess.run(
            ["avahi-resolve-host-name", "-4", f"{hostname}.local"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            # Returns "hostname.local	192.168.x.x"
            return result.stdout.strip()
    except:
        pass
    
    # Try generic mDNS lookup
    try:
        result = subprocess.run(
            ["avahi-browse", "-t", "-r", "-A"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0 and hostname in result.stdout:
            return result.stdout
    except:
        pass
    
    return None


def get_device_info_async(ip, hostname, vendor, mac, config, cache, cache_lock, get_snmp_func):
    """
    Get device info asynchronously (SNMP + mDNS)
    
    Args:
        ip: IP address
        hostname: Hostname
        vendor: MAC vendor
        mac: MAC address
        config: Configuration dict
        cache: Device info cache
        cache_lock: Threading lock for cache
        get_snmp_func: Function to get SNMP info
    
    Returns:
        dict: Device information (snmp, mdns)
    """
    cache_key = f"{ip}:{hostname}"
    
    with cache_lock:
        if cache_key in cache:
            return cache[cache_key]
    
    info = {
        "snmp": None,
        "mdns": None
    }
    
    # Fetch in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        snmp_future = executor.submit(get_snmp_func, ip) if config.get('enable_snmp') else None
        mdns_future = executor.submit(get_mdns_info, hostname) if config.get('enable_mdns') else None
        
        if snmp_future:
            try:
                info["snmp"] = snmp_future.result(timeout=config.get('snmp_timeout', 1))
            except:
                pass
        
        if mdns_future:
            try:
                info["mdns"] = mdns_future.result(timeout=config.get('mdns_timeout', 1))
            except:
                pass
    
    with cache_lock:
        cache[cache_key] = info
    
    return info


def format_timestamp(timestamp):
    """
    Format UNIX timestamp to readable date/time
    
    Args:
        timestamp: UNIX timestamp
    
    Returns:
        Formatted date string
    """
    try:
        dt = datetime.fromtimestamp(int(timestamp))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(timestamp)


def format_duration(seconds):
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string
    """
    try:
        seconds = int(seconds)
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m"
        elif seconds < 86400:
            return f"{seconds // 3600}h"
        else:
            return f"{seconds // 86400}d"
    except:
        return str(seconds)


def safe_int(value, default=0):
    """
    Safely convert value to int
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        int value
    """
    try:
        return int(value)
    except:
        return default


def safe_float(value, default=0.0):
    """
    Safely convert value to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        float value
    """
    try:
        return float(value)
    except:
        return default
