"""Device type detection and classification"""


SERVICE_ICONS = {
    '22': ('🔑', 'SSH'),
    '25': ('✉️', 'SMTP'),
    '53': ('🔍', 'DNS'),
    '80': ('🌐', 'HTTP'),
    '110': ('📧', 'POP3'),
    '143': ('📧', 'IMAP'),
    '161': ('📊', 'SNMP'),
    '389': ('👤', 'LDAP'),
    '443': ('🔒', 'HTTPS'),
    '631': ('🖨️', 'CUPS'),
    '3000': ('📊', 'Web'),
    '3306': ('🗄️', 'MySQL'),
    '5000': ('📊', 'Flask'),
    '5432': ('🗄️', 'PostgreSQL'),
    '5900': ('👁️', 'VNC'),
    '6379': ('⚡', 'Redis'),
    '8000': ('🌐', 'HTTP'),
    '8080': ('🌐', 'HTTP-Alt'),
    '8443': ('🔒', 'HTTPS-Alt'),
    '8888': ('🌐', 'HTTP'),
    '9000': ('🎯', 'Admin'),
    '9090': ('📊', 'Admin'),
}


def format_service_link(ip, port_service, service_name):
    """Format service with icon and clickable link if applicable"""
    port = port_service.split('/')[0]
    
    if port in SERVICE_ICONS:
        icon, label = SERVICE_ICONS[port]
    else:
        icon, label = '⚙️', service_name[:15]
    
    if port in ['80', '443', '8080', '8443', '3000', '5000', '8000', '8888', '9000', '9090']:
        protocol = 'https' if port in ['443', '8443'] else 'http'
        url = f"{protocol}://{ip}:{port}"
        return f"{icon} <a href='{url}' target='_blank' class='service-link'>{port}</a>"
    else:
        return f"{icon} {port}"


def get_device_type(hostname, vendor, mac, device_info=None):
    """Detect device type from all available sources"""
    h = hostname.lower() if hostname and hostname != "N/A" else ""
    v = vendor.lower() if vendor else ""
    m = mac.lower() if mac else ""
    
    combined = f"{h} {v} {m}"
    
    if device_info:
        if device_info.get("snmp"):
            combined += f" {device_info['snmp'].lower()}"
        if device_info.get("mdns"):
            combined += f" {device_info['mdns'].lower()}"
    
    # Cameras
    if any(x in combined for x in ["dafang", "camera", "webcam", "hikvision", "dahua", "reolink", "wyze", "ring", "doorbell", "video", "ipcam", "cam-"]):
        return ("📷", "Camera")
    
    # Samsung devices
    if "samsung" in v or "s24" in h or "galaxy" in h or "tab-a" in h or "sm-" in h:
        if any(x in h for x in ["tab", "tablet"]):
            return ("📱", "Samsung Tablet")
        elif any(x in h for x in ["s24", "s23", "s22", "s21", "s20", "galaxy", "phone"]):
            return ("📱", "Samsung Phone")
        elif "tv" in h:
            return ("📺", "Samsung TV")
        else:
            return ("📱", "Samsung")
    
    # Apple devices
    if any(x in h for x in ["macbook", "imac", "mac-", "iphone", "ipad"]):
        if "macbook" in h or "imac" in h or "mac" in h:
            return ("🍎", "Apple Mac")
        elif "iphone" in h:
            return ("🍎", "iPhone")
        elif "ipad" in h:
            return ("🍎", "iPad")
        else:
            return ("🍎", "Apple")
    
    if any(x in v for x in ["apple"]):
        return ("🍎", "Apple")
    
    # Amazon devices
    if "amazon" in v:
        if any(x in combined for x in ["echo", "alexa", "dot"]):
            return ("🔊", "Amazon Echo")
        elif any(x in combined for x in ["fire", "firetv", "stick"]):
            return ("📺", "Fire TV")
        else:
            return ("📦", "Amazon Device")
    
    # TV & Media devices
    if any(x in h for x in ["tv", "tele", "television"]):
        if "philips" in combined or "phillips" in combined:
            return ("📺", "Philips TV")
        elif "samsung" in combined:
            return ("📺", "Samsung TV")
        elif "lg" in combined:
            return ("📺", "LG TV")
        else:
            return ("📺", "TV")
    
    if any(x in combined for x in ["samsung tv", "lg tv", "sony tv", "philips", "panasonic", "toshiba", "vizio", "roku", "firestick", "appletv", "android tv", "smarttv", "hisense", "sharp"]):
        return ("📺", "TV")
    
    # Smartphones
    if any(x in h for x in ["phone", "mobile", "pixel", "oneplus", "redmi"]):
        return ("📱", "Smartphone")
    
    if any(x in combined for x in ["android", "pixel", "htc", "motorola", "oneplus", "redmi", "realme", "oppo", "vivo"]):
        return ("📱", "Smartphone")
    
    # Tablets
    if any(x in h for x in ["tablet", "tab-", "ipad"]):
        return ("📱", "Tablet")
    
    # Xiaomi devices
    if "xiaomi" in v:
        if any(x in h for x in ["camera", "cam", "dafang"]):
            return ("📷", "Xiaomi Camera")
        elif any(x in h for x in ["phone", "redmi", "mi-", "poco"]):
            return ("📱", "Xiaomi Phone")
        elif "tv" in h:
            return ("📺", "Xiaomi TV")
        else:
            return ("🔌", "Xiaomi Device")
    
    # Routers & Network
    if any(x in combined for x in ["router", "gateway", "access point", "ap-", "ap_", "wifi", "ubiquiti", "tp-link", "netgear", "cisco", "asus", "linksys", "mikrotik", "fortinet", "d-link", "meraki", "ieee registration authority"]):
        return ("📡", "Router/AP")
    
    # Printers
    if any(x in combined for x in ["print", "brother", "hp", "xerox", "canon", "epson", "ricoh", "konica", "minolta"]):
        return ("🖨️", "Printer")
    
    # Smart Home & IoT
    if any(x in combined for x in ["esp", "esp32", "esp8266", "esp8285", "espressif", "arduino", "home", "smart", "homekit", "zigbee", "zwave", "mqtt", "sonoff", "shelly", "tasmota", "tuya"]):
        return ("🔌", "Smart Home")
    
    # Laptops & Desktops
    if any(x in combined for x in ["laptop", "desktop", "pc", "computer", "dell", "hp", "lenovo", "asus", "acer", "msi", "windows", "linux", "workstation"]):
        return ("💻", "Computer")
    
    # Raspberry Pi & SBC
    if any(x in combined for x in ["raspi", "raspberry", "rpi", "pi", "jetson", "odroid", "beaglebone"]):
        return ("🍓", "Raspberry Pi")
    
    # Servers & NAS
    if any(x in combined for x in ["server", "nas", "synology", "qnap", "pfsense", "proxmox", "homelab", "unraid"]):
        return ("⚙️", "Server/NAS")
    
    # Smart TVs & Media Players
    if any(x in combined for x in ["chromecast", "nvidia shield", "kodi", "plex", "media"]):
        return ("📺", "Media Player")
    
    # Gaming
    if any(x in combined for x in ["gaming", "xbox", "playstation", "ps4", "ps5", "nintendo", "steam", "switch"]):
        return ("🎮", "Gaming")
    
    # Audio & Speakers
    if any(x in combined for x in ["speaker", "audio", "sonos", "bose", "harman", "denon", "yamaha", "amplifier"]):
        return ("🔊", "Audio")
    
    # Smartwatch & Wearables
    if any(x in combined for x in ["watch", "fitbit", "garmin", "smartband", "wearable"]):
        return ("⌚", "Wearable")
    
    # Scanners
    if any(x in combined for x in ["scanner", "mfp", "multifunction"]):
        return ("📄", "Scanner")
    
    # Network Storage
    if any(x in combined for x in ["storage", "backup", "hdd", "ssd"]):
        return ("💾", "Storage")
    
    # Chinese tech company devices
    if "hui zhou gaoshengda" in v or "gaoshengda" in v:
        if "tv" in h or "tele" in h:
            return ("📺", "TV Box")
        else:
            return ("📺", "Media Box")
    
    return ("❓", "Unknown")
