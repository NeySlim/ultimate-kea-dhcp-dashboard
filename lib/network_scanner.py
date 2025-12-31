"""Network scanning module for device and service discovery"""
import subprocess
import socket
import time
from concurrent.futures import ThreadPoolExecutor


def ping_host(ip):
    """Check if host is alive using ping"""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            capture_output=True,
            timeout=2
        )
        return result.returncode == 0
    except Exception:
        return False


def get_mac_from_arp(ip):
    """Retrieve MAC address from ARP cache"""
    try:
        result = subprocess.run(
            ["ip", "neigh", "show", ip],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.split()
            for i, part in enumerate(parts):
                if part == "lladdr" and i + 1 < len(parts):
                    mac = parts[i + 1]
                    if ':' in mac:
                        return mac.upper()
        
        result = subprocess.run(
            ["arp", "-n", ip],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if ip in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        mac = parts[2]
                        if ':' in mac and mac != "(incomplete)":
                            return mac.upper()
    except Exception:
        pass
    return None


def get_hostname_from_reverse_dns(ip):
    """Resolve hostname via reverse DNS"""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        if hostname:
            return hostname
    except Exception:
        pass
    return None


def get_hostname_from_snmp(ip, community="public", timeout=2):
    """Retrieve hostname via SNMP"""
    try:
        result = subprocess.run(
            ["snmpget", "-v2c", "-c", community, "-Oqv", "-t", str(timeout), ip, "SNMPv2-MIB::sysName.0"],
            capture_output=True,
            text=True,
            timeout=timeout+1
        )
        if result.returncode == 0:
            hostname = result.stdout.strip().strip('"')
            if hostname and hostname != "No Such Object available on this agent at this OID":
                return hostname
    except Exception:
        pass
    return None


def scan_network_host(ip, timeout=5):
    """Scan host for open ports and services using nmap"""
    try:
        result = subprocess.run(
            ["nmap", "-sV", "-p", "22,80,443,3000,8000,8080,8443,9000,5000,5900,631,3306,5432,25,53,110,143,161,389,6379", 
             "--open", "--max-retries", "2", "--host-timeout", "30s",
             "--max-rtt-timeout", "2000ms", "--initial-rtt-timeout", "500ms", 
             "-T4", "-n", ip],
            capture_output=True,
            text=True,
            timeout=timeout+30
        )
        
        services = []
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if '/tcp' in line and 'open' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        port_service = parts[0]
                        status = parts[1]
                        service = ' '.join(parts[2:]) if len(parts) > 2 else "Unknown"
                        services.append({
                            "port": port_service,
                            "status": status,
                            "service": service
                        })
        
        return services
    except Exception:
        return []


def scan_static_device_enhanced(ip, snmp_community="public"):
    """Enhanced scan for static devices using multiple methods"""
    data = {
        'hostname': None,
        'mac': None,
        'vendor': None,
        'services': [],
        'alive': False
    }
    
    data['alive'] = ping_host(ip)
    
    if not data['alive']:
        return data
    
    time.sleep(0.1)
    
    mac = get_mac_from_arp(ip)
    if mac:
        data['mac'] = mac
    
    hostname = get_hostname_from_reverse_dns(ip)
    if hostname:
        data['hostname'] = hostname
    
    if not data['hostname']:
        snmp_hostname = get_hostname_from_snmp(ip, snmp_community)
        if snmp_hostname:
            data['hostname'] = snmp_hostname
    
    data['services'] = scan_network_host(ip)
    
    return data


def get_snmp_sysDescr(ip, community="public", timeout=1):
    """Get SNMP sysDescr from device"""
    try:
        result = subprocess.run(
            ["snmpget", "-v", "2c", "-c", community, "-t", str(timeout), ip, "1.3.6.1.2.1.1.1.0"],
            capture_output=True,
            text=True,
            timeout=timeout+1
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if lines:
                for line in lines:
                    if "STRING:" in line:
                        return line.split("STRING:")[-1].strip().strip('"')
    except Exception:
        pass
    return None
