#!/bin/bash
###############################################################################
# Ultimate Kea Dashboard - Dependency Check Script
# Vérifie que toutes les dépendances sont installées
###############################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Ultimate Kea Dashboard${NC}"
echo -e "${BLUE}Dependency Check${NC}"
echo -e "${BLUE}========================================${NC}\n"

MISSING_REQUIRED=0
MISSING_OPTIONAL=0

check_command() {
    local cmd=$1
    local name=$2
    local required=$3
    
    if command -v $cmd &> /dev/null; then
        echo -e "${GREEN}✓${NC} $name"
        return 0
    else
        if [ "$required" = "yes" ]; then
            echo -e "${RED}✗${NC} $name (REQUIS)"
            MISSING_REQUIRED=$((MISSING_REQUIRED + 1))
        else
            echo -e "${YELLOW}⚠${NC} $name (optionnel)"
            MISSING_OPTIONAL=$((MISSING_OPTIONAL + 1))
        fi
        return 1
    fi
}

check_python_module() {
    local module=$1
    local name=$2
    local required=$3
    
    if python3 -c "import $module" 2>/dev/null; then
        VERSION=$(python3 -c "import $module; print($module.__version__)" 2>/dev/null)
        echo -e "${GREEN}✓${NC} $name${VERSION:+ (version: $VERSION)}"
        return 0
    else
        if [ "$required" = "yes" ]; then
            echo -e "${RED}✗${NC} $name (REQUIS)"
            MISSING_REQUIRED=$((MISSING_REQUIRED + 1))
        else
            echo -e "${YELLOW}⚠${NC} $name (optionnel)"
            MISSING_OPTIONAL=$((MISSING_OPTIONAL + 1))
        fi
        return 1
    fi
}

echo -e "${YELLOW}Dépendances Système Requises :${NC}"
check_command python3 "Python 3" yes
check_command pip3 "pip3" yes || check_command pip "pip" yes
check_command nmap "Nmap" yes
check_command ping "Ping" yes
check_command ip "IP command" yes
check_command arp "ARP command" yes

echo -e "\n${YELLOW}Dépendances Python Requises :${NC}"
check_python_module psutil "psutil" yes

echo -e "\n${YELLOW}Dépendances Optionnelles (fonctionnalités avancées) :${NC}"
check_command snmpget "SNMP tools" no
check_command avahi-resolve-host-name "Avahi mDNS" no

echo -e "\n${YELLOW}Vérification des Chemins Kea DHCP :${NC}"
if [ -d "/etc/kea" ]; then
    echo -e "${GREEN}✓${NC} /etc/kea (configuration directory exists)"
else
    echo -e "${YELLOW}⚠${NC} /etc/kea (directory not found - Kea may not be installed)"
fi

if [ -d "/var/lib/kea" ]; then
    echo -e "${GREEN}✓${NC} /var/lib/kea (leases directory exists)"
else
    echo -e "${YELLOW}⚠${NC} /var/lib/kea (directory not found - Kea may not be installed)"
fi

if [ -d "/run/kea" ]; then
    echo -e "${GREEN}✓${NC} /run/kea (socket directory exists)"
elif [ -S "/run/kea/kea4-ctrl-socket" ]; then
    echo -e "${GREEN}✓${NC} /run/kea/kea4-ctrl-socket (socket exists)"
else
    echo -e "${YELLOW}⚠${NC} /run/kea (directory not found - Kea may not be running)"
fi

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}Résumé${NC}"
echo -e "${BLUE}========================================${NC}\n"

if [ $MISSING_REQUIRED -eq 0 ]; then
    echo -e "${GREEN}✓ Toutes les dépendances requises sont installées${NC}"
else
    echo -e "${RED}✗ $MISSING_REQUIRED dépendance(s) requise(s) manquante(s)${NC}"
fi

if [ $MISSING_OPTIONAL -gt 0 ]; then
    echo -e "${YELLOW}⚠ $MISSING_OPTIONAL dépendance(s) optionnelle(s) manquante(s)${NC}"
    echo -e "  Les fonctionnalités avancées (SNMP, mDNS) seront désactivées"
fi

echo ""

if [ $MISSING_REQUIRED -gt 0 ]; then
    echo -e "${RED}Installation nécessaire !${NC}"
    echo -e "Exécutez : ${YELLOW}sudo bash install.sh${NC}"
    exit 1
else
    echo -e "${GREEN}Système prêt !${NC}"
    echo -e "Vous pouvez démarrer le dashboard avec : ${YELLOW}sudo systemctl start ultimate-kea-dashboard${NC}"
    exit 0
fi
