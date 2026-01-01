# Dépendances Optionnelles

Ultimate Kea Dashboard fonctionne avec des dépendances de base, mais certaines fonctionnalités avancées nécessitent des packages supplémentaires.

## Dépendances Requises

Ces packages sont **obligatoires** et installés automatiquement :

| Package | Debian/Ubuntu | Fedora/RHEL | Arch | Fonction |
|---------|---------------|-------------|------|----------|
| Python 3 | `python3` | `python3` | `python` | Exécution du dashboard |
| Python pip | `python3-pip` | `python3-pip` | `python-pip` | Gestion des dépendances Python (optionnel) |
| **psutil** (Python) | `python3-psutil` | `python3-psutil` | `python-psutil` | **Métriques système** (CPU, RAM, réseau, disque) |
| Nmap | `nmap` | `nmap` | `nmap` | Scan réseau et détection de services |
| IP utils | `iputils-ping` | `iputils` | `iputils` | Commandes réseau (ping) |
| Net tools | `net-tools` | `net-tools` | `net-tools` | Commande ARP |

### Dépendance Python Critique : psutil

**psutil** est une bibliothèque Python **obligatoire** pour les métriques système en temps réel.

**Installation recommandée (via packages système)** :

```bash
# Debian/Ubuntu
sudo apt install python3-psutil

# Fedora
sudo dnf install python3-psutil

# RHEL/CentOS/Rocky/AlmaLinux
sudo dnf install python3-psutil  # Via EPEL

# Arch/Manjaro
sudo pacman -S python-psutil

# openSUSE
sudo zypper install python3-psutil
```

**Pourquoi préférer les packages système ?**
- ✅ Intégration avec le gestionnaire de paquets
- ✅ Mises à jour automatiques
- ✅ Pas de conflit avec pip
- ✅ Compatible avec PEP 668 (Debian 12+, Ubuntu 23.04+)
- ✅ Pas besoin de --break-system-packages

**Installation alternative (via pip)** :

Uniquement si le package système n'est pas disponible ou pour environnement de développement.

```bash
# Méthode standard (peut échouer sur Debian 12+/Ubuntu 23.04+)
pip3 install psutil

# Sur distributions récentes (PEP 668)
pip3 install --break-system-packages psutil

# OU utiliser un environnement virtuel (recommandé pour dev)
python3 -m venv venv
source venv/bin/activate
pip install psutil
```

**Si absent** : Les métriques système (CPU, RAM, réseau, disque) ne fonctionneront pas. Le dashboard retournera des valeurs à 0.

**Version minimale** : psutil >= 5.8.0

**Disponibilité** : Disponible dans les dépôts officiels de toutes les distributions supportées

## Dépendances Optionnelles

Ces packages activent des fonctionnalités supplémentaires mais ne sont **pas obligatoires** :

### SNMP (Simple Network Management Protocol)

**Fonction** : Récupération avancée d'informations sur les équipements réseau (nom d'hôte, description système)

| Distribution | Package |
|--------------|---------|
| Debian/Ubuntu | `snmp` |
| Fedora/RHEL/CentOS | `net-snmp-utils` |
| Arch/Manjaro | `net-snmp` |
| openSUSE | `net-snmp` |

**Installation manuelle** :
```bash
# Debian/Ubuntu
sudo apt install snmp

# Fedora/RHEL/CentOS
sudo dnf install net-snmp-utils

# Arch
sudo pacman -S net-snmp

# openSUSE
sudo zypper install net-snmp
```

**Commandes utilisées** : `snmpget`

**Si absent** : La récupération du nom d'hôte via SNMP sera désactivée. Le dashboard utilisera uniquement le reverse DNS.

### Avahi (mDNS/Zeroconf)

**Fonction** : Découverte de services sur le réseau local (imprimantes, serveurs NAS, etc.)

| Distribution | Package |
|--------------|---------|
| Debian/Ubuntu | `avahi-utils` |
| Fedora/RHEL/CentOS | `avahi-tools` |
| Arch/Manjaro | `avahi` |
| openSUSE | `avahi-utils` |

**Installation manuelle** :
```bash
# Debian/Ubuntu
sudo apt install avahi-utils

# Fedora/RHEL/CentOS
sudo dnf install avahi-tools

# Arch
sudo pacman -S avahi

# openSUSE
sudo zypper install avahi-utils
```

**Commandes utilisées** : `avahi-resolve-host-name`, `avahi-browse`

**Si absent** : La découverte mDNS sera désactivée. Pas d'impact majeur sur les fonctionnalités principales.

**Note Arch** : Le daemon Avahi doit être démarré :
```bash
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
```

## Matrice de Fonctionnalités

| Fonctionnalité | Dépendance | Critique |
|----------------|------------|----------|
| Affichage des leases DHCP | Aucune (lecture CSV) | ✅ Oui |
| **Métriques système (CPU, RAM, etc.)** | **psutil (Python)** | ✅ **Oui** |
| Scan réseau (ports ouverts) | nmap | ✅ Oui |
| Ping des hôtes | iputils | ✅ Oui |
| Récupération MAC depuis ARP | net-tools | ✅ Oui |
| Reverse DNS | Python socket | ✅ Oui |
| Identification du vendeur MAC | Base de données OUI | ✅ Oui |
| SNMP hostname | snmp/net-snmp-utils | ⚠️ Optionnel |
| SNMP sysDescr | snmp/net-snmp-utils | ⚠️ Optionnel |
| mDNS discovery | avahi-utils/avahi-tools | ⚠️ Optionnel |

## Configuration

Pour désactiver les fonctionnalités optionnelles si les packages ne sont pas installés, éditez `/etc/ultimate-dashboard/ultimate-dashboard.conf` :

```ini
[DEFAULT]
# Désactiver SNMP
enable_snmp = false
snmp_community = public
snmp_timeout = 1

# Désactiver mDNS
enable_mdns = false
mdns_timeout = 1
```

## Vérification

Pour vérifier quelles commandes sont disponibles sur votre système :

```bash
# Commandes requises
command -v python3 && echo "✓ Python 3"
command -v nmap && echo "✓ Nmap"
command -v ping && echo "✓ Ping"
command -v arp && echo "✓ ARP"

# Dépendance Python critique
python3 -c "import psutil; print('✓ psutil version:', psutil.__version__)" 2>/dev/null || echo "✗ psutil non installé"

# Commandes optionnelles
command -v snmpget && echo "✓ SNMP" || echo "✗ SNMP non disponible"
command -v avahi-resolve-host-name && echo "✓ Avahi" || echo "✗ Avahi non disponible"
```

## Performance

Les fonctionnalités optionnelles peuvent impacter les performances :

| Fonctionnalité | Impact | Timeout par défaut |
|----------------|--------|-------------------|
| Reverse DNS | Moyen | 2 secondes |
| SNMP | Moyen | 1 seconde |
| mDNS | Faible | 1 seconde |
| Scan Nmap | Élevé | 5 secondes (configurable) |

Pour améliorer les performances, ajustez les timeouts dans la configuration :

```ini
[DEFAULT]
reverse_dns_timeout = 1
snmp_timeout = 0.5
mdns_timeout = 0.5
scanner_timeout = 3
```

## Installation Automatique

L'installateur officiel tente d'installer les packages optionnels automatiquement. Si l'installation échoue, le dashboard fonctionne quand même avec les fonctionnalités de base.

```bash
# L'installateur essaie d'installer tous les packages
sudo bash install.sh

# Vérifiez les warnings pendant l'installation
# "Optional packages (...) not installed - some features may be limited"
```

### Réinstallation des Packages Optionnels

Si vous avez installé le dashboard sans les packages optionnels, vous pouvez les ajouter plus tard :

```bash
# Debian/Ubuntu
sudo apt install snmp avahi-utils

# Fedora/RHEL/CentOS
sudo dnf install net-snmp-utils avahi-tools

# Arch
sudo pacman -S net-snmp avahi
sudo systemctl enable --now avahi-daemon

# openSUSE
sudo zypper install net-snmp avahi-utils
```

**Pour réinstaller psutil (si manquant)** :

**Méthode recommandée (packages système)** :

```bash
# Debian/Ubuntu
sudo apt install python3-psutil

# Fedora/RHEL/CentOS
sudo dnf install python3-psutil

# Arch/Manjaro
sudo pacman -S python-psutil

# openSUSE
sudo zypper install python3-psutil
```

**Méthode alternative (pip - non recommandée pour production)** :

```bash
# Debian/Ubuntu (anciennes versions)
pip3 install psutil

# Debian 12+/Ubuntu 23.04+ (nécessite flag spécial)
pip3 install --break-system-packages psutil

# Arch (déconseillé - utiliser pacman)
pip install --user psutil

# Pour développement (recommandé)
python3 -m venv venv
source venv/bin/activate
pip install psutil
```

Puis redémarrez le dashboard :

```bash
sudo systemctl restart ultimate-dashboard
```

## Compatibilité

Toutes les distributions Linux supportées utilisent les mêmes commandes de base. Les différences résident uniquement dans les noms des packages.

## Dépannage

### SNMP ne fonctionne pas

```bash
# Vérifier l'installation
snmpget --version

# Tester manuellement
snmpget -v2c -c public <IP> SNMPv2-MIB::sysName.0

# Vérifier la configuration du pare-feu (port UDP 161)
```

### Avahi ne fonctionne pas

```bash
# Vérifier le daemon (surtout sur Arch)
sudo systemctl status avahi-daemon

# Démarrer si nécessaire
sudo systemctl start avahi-daemon

# Tester manuellement
avahi-browse -a -t
```

### ARP cache vide

```bash
# Forcer un ping pour remplir le cache ARP
ping -c 1 <IP>

# Vérifier le cache
ip neigh show
# ou
arp -n
```

## Recommandations

Pour une expérience optimale :

1. **Réseau d'entreprise** : Installer SNMP pour une meilleure identification des équipements
2. **Réseau domestique** : Installer Avahi pour la découverte automatique
3. **Environnement restreint** : Les dépendances de base suffisent
4. **Performance** : Désactiver les fonctionnalités non utilisées

## Chemins Standards

Tous les chemins système utilisés sont conformes au FHS (Filesystem Hierarchy Standard) et identiques sur toutes les distributions :

- Configuration Kea : `/etc/kea/`
- Leases Kea : `/var/lib/kea/`
- Socket Kea : `/run/kea/`
- Configuration Dashboard : `/etc/ultimate-dashboard/`
- Installation Dashboard : `/opt/ultimate-kea-dashboard/`

**Aucune adaptation de chemins n'est nécessaire entre distributions.**
