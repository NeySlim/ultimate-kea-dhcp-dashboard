# Installation sur Arch Linux

Guide d'installation spécifique pour Arch Linux et dérivés (Manjaro, EndeavourOS).

## Prérequis

- Arch Linux, Manjaro ou EndeavourOS
- Accès root ou sudo
- Serveur ISC Kea DHCP installé

## Installation rapide

```bash
# Télécharger l'installateur
curl -sL https://raw.githubusercontent.com/NeySlim/ultimate-kea-dhcp-dashboard/main/install.sh -o install.sh

# Exécuter l'installation
sudo bash install.sh
```

L'installateur détectera automatiquement Arch Linux et utilisera Pacman.

## Installation manuelle

### 1. Installer les dépendances

```bash
# Mettre à jour le système
sudo pacman -Syu

# Installer les paquets requis
sudo pacman -S nmap iputils python python-pip git net-tools

# Installer les paquets optionnels (recommandés)
sudo pacman -S net-snmp avahi

# Activer le daemon Avahi
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
```

**Paquets optionnels** :
- `net-snmp` : Permet la récupération d'informations via SNMP
- `avahi` : Active la découverte mDNS/Zeroconf (daemon requis)

Le dashboard fonctionne sans ces paquets mais avec moins de fonctionnalités. Voir [DEPENDENCIES.md](DEPENDENCIES.md) pour plus de détails.

### 2. Cloner le dépôt

```bash
git clone https://github.com/NeySlim/ultimate-kea-dashboard.git
cd ultimate-kea-dashboard
```

### 3. Exécuter l'installateur

```bash
sudo bash install.sh
```

## Installation via AUR (à venir)

Un paquet AUR sera bientôt disponible :

```bash
# Avec yay
yay -S ultimate-kea-dashboard

# Avec paru
paru -S ultimate-kea-dashboard
```

## Configuration du pare-feu

### Avec firewalld

```bash
# Installer firewalld si nécessaire
sudo pacman -S firewalld

# Démarrer et activer firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Ouvrir le port
sudo firewall-cmd --permanent --add-port=8089/tcp
sudo firewall-cmd --reload
```

### Avec iptables

```bash
# Installer iptables si nécessaire
sudo pacman -S iptables

# Ajouter la règle
sudo iptables -A INPUT -p tcp --dport 8089 -j ACCEPT

# Sauvegarder les règles
sudo iptables-save > /etc/iptables/iptables.rules

# Activer iptables au démarrage
sudo systemctl enable iptables
sudo systemctl start iptables
```

### Avec nftables (recommandé sur Arch)

```bash
# Éditer la configuration
sudo nano /etc/nftables.conf
```

Ajouter :

```
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        
        # Autoriser loopback
        iif lo accept
        
        # Autoriser les connexions établies
        ct state established,related accept
        
        # Autoriser SSH
        tcp dport 22 accept
        
        # Autoriser le dashboard
        tcp dport 8089 accept
    }
}
```

Activer :

```bash
sudo systemctl enable nftables
sudo systemctl start nftables
```

## Certificats SSL

Sur Arch, créez vos certificats auto-signés :

```bash
# Créer les répertoires
sudo mkdir -p /etc/ssl/private /etc/ssl/certs

# Générer le certificat
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/ssl-cert-snakeoil.key \
  -out /etc/ssl/certs/ssl-cert-snakeoil.pem

# Permissions
sudo chmod 600 /etc/ssl/private/ssl-cert-snakeoil.key
```

## Service systemd

### Créer le service

Le fichier est créé automatiquement dans `/etc/systemd/system/ultimate-dashboard.service`.

```ini
[Unit]
Description=Ultimate Kea DHCP Dashboard
After=network.target kea-dhcp4.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ultimate-kea-dashboard
ExecStart=/usr/bin/python /opt/ultimate-kea-dashboard/bin/ultimate-dashboard
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Gérer le service

```bash
# Recharger systemd
sudo systemctl daemon-reload

# Démarrer le service
sudo systemctl start ultimate-dashboard

# Activer au démarrage
sudo systemctl enable ultimate-dashboard

# Vérifier le statut
sudo systemctl status ultimate-dashboard

# Voir les logs
sudo journalctl -u ultimate-dashboard -f

# Redémarrer
sudo systemctl restart ultimate-dashboard
```

## Configuration de Kea DHCP

### Installer Kea DHCP

```bash
sudo pacman -S kea
```

### Emplacement des fichiers

```bash
# Configuration
/etc/kea/kea-dhcp4.conf

# Leases
/var/lib/kea/kea-leases4.csv

# Socket de contrôle
/run/kea/kea4-ctrl-socket
```

### Activer le socket de contrôle

Éditez `/etc/kea/kea-dhcp4.conf` :

```json
{
  "Dhcp4": {
    "control-socket": {
      "socket-type": "unix",
      "socket-name": "/run/kea/kea4-ctrl-socket"
    },
    "lease-database": {
      "type": "memfile",
      "persist": true,
      "name": "/var/lib/kea/kea-leases4.csv"
    }
  }
}
```

Démarrer Kea :

```bash
sudo systemctl enable kea-dhcp4
sudo systemctl start kea-dhcp4
```

## Spécificités Arch Linux

### Python

Sur Arch, `python` pointe vers Python 3. Pas besoin de `python3`.

```bash
python --version  # Python 3.x
```

### Gestion des paquets

Arch utilise un système de rolling release :

```bash
# Toujours mettre à jour avant d'installer
sudo pacman -Syu

# Installer un paquet
sudo pacman -S package_name

# Rechercher un paquet
pacman -Ss keyword

# Informations sur un paquet
pacman -Si package_name
```

### AUR Helper

Pour les paquets AUR, utilisez un helper :

```bash
# Installer yay
sudo pacman -S --needed git base-devel
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

## Dépannage

### Problèmes de Python

```bash
# Vérifier la version
python --version

# Réinstaller Python
sudo pacman -S python python-pip
```

### Permissions de socket Kea

```bash
# Vérifier le socket
ls -la /run/kea/

# Ajuster les permissions si nécessaire
sudo chmod 666 /run/kea/kea4-ctrl-socket
```

### Le service ne démarre pas

```bash
# Logs détaillés
sudo journalctl -u ultimate-dashboard -xe

# Vérifier les dépendances
ldd /usr/bin/python

# Tester manuellement
sudo python /opt/ultimate-kea-dashboard/bin/ultimate-dashboard
```

### Conflit de ports

```bash
# Vérifier quel processus utilise le port
sudo lsof -i :8089

# Ou avec ss
sudo ss -tulpn | grep 8089
```

## Mise à jour

### Via Git

```bash
cd ultimate-kea-dashboard
git pull
sudo bash install.sh
sudo systemctl restart ultimate-dashboard
```

### Via AUR (quand disponible)

```bash
yay -Syu ultimate-kea-dashboard
```

## Optimisations Arch

### Utiliser un utilisateur dédié (recommandé)

```bash
# Créer un utilisateur système
sudo useradd -r -s /bin/false ultimate-dashboard

# Ajuster le service
sudo nano /etc/systemd/system/ultimate-dashboard.service
```

Modifier :
```ini
User=ultimate-dashboard
Group=ultimate-dashboard
```

Ajuster les permissions :
```bash
sudo chown -R ultimate-dashboard:ultimate-dashboard /opt/ultimate-kea-dashboard
sudo chown -R ultimate-dashboard:ultimate-dashboard /etc/ultimate-dashboard
```

### Systemd hardening

Ajouter dans le service :

```ini
[Service]
# Sécurité
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/kea /run/kea /var/log/ultimate-dashboard

# Capacités réseau
CapabilityBoundingSet=CAP_NET_RAW CAP_NET_ADMIN
AmbientCapabilities=CAP_NET_RAW CAP_NET_ADMIN
```

## Désinstallation

```bash
# Arrêter et désactiver le service
sudo systemctl stop ultimate-dashboard
sudo systemctl disable ultimate-dashboard

# Supprimer les fichiers
sudo rm -rf /opt/ultimate-kea-dashboard
sudo rm -rf /etc/ultimate-dashboard
sudo rm /etc/systemd/system/ultimate-dashboard.service

# Recharger systemd
sudo systemctl daemon-reload

# Supprimer les paquets (optionnel)
sudo pacman -Rns nmap iputils
```

## Wiki Arch

Pour plus d'informations sur la configuration réseau et systemd :
- https://wiki.archlinux.org/title/Systemd
- https://wiki.archlinux.org/title/Nftables
- https://wiki.archlinux.org/title/ISC_Kea

## Support

Pour les problèmes spécifiques à Arch : https://github.com/NeySlim/ultimate-kea-dashboard/issues
