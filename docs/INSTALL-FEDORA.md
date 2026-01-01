# Installation sur Fedora

Guide d'installation spécifique pour Fedora Linux.

## Prérequis

- Fedora 35 ou supérieur
- Accès root ou sudo
- Serveur ISC Kea DHCP installé

## Installation rapide

```bash
# Télécharger l'installateur
curl -sL https://raw.githubusercontent.com/NeySlim/ultimate-kea-dhcp-dashboard/main/install.sh -o install.sh

# Exécuter l'installation
sudo bash install.sh
```

L'installateur détectera automatiquement Fedora et utilisera DNF.

## Installation manuelle

### 1. Installer les dépendances

```bash
# Mettre à jour le système
sudo dnf update

# Installer les paquets requis
sudo dnf install -y nmap iputils python3 python3-pip git net-tools

# Installer les paquets optionnels (recommandés)
sudo dnf install -y net-snmp-utils avahi-tools
```

**Paquets optionnels** :
- `net-snmp-utils` : Permet la récupération d'informations via SNMP
- `avahi-tools` : Active la découverte mDNS/Zeroconf

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

Ou copier manuellement les fichiers :

```bash
# Créer les répertoires
sudo mkdir -p /opt/ultimate-kea-dashboard/{bin,lib,static,data,logs,etc}
sudo mkdir -p /etc/ultimate-dashboard

# Copier les fichiers
sudo cp -r bin/* /opt/ultimate-kea-dashboard/bin/
sudo cp -r lib/* /opt/ultimate-kea-dashboard/lib/
sudo cp -r static/* /opt/ultimate-kea-dashboard/static/
sudo cp -r data/* /opt/ultimate-kea-dashboard/data/
sudo cp start.sh /opt/ultimate-kea-dashboard/

# Rendre les scripts exécutables
sudo chmod +x /opt/ultimate-kea-dashboard/bin/ultimate-dashboard
sudo chmod +x /opt/ultimate-kea-dashboard/start.sh
```

## Configuration du pare-feu

Fedora utilise firewalld par défaut :

```bash
# Ouvrir le port 8089
sudo firewall-cmd --permanent --add-port=8089/tcp
sudo firewall-cmd --reload

# Vérifier
sudo firewall-cmd --list-ports
```

Pour HTTPS (port 8089 avec SSL) :

```bash
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## Configuration SELinux

Si SELinux est activé (par défaut sur Fedora), configurez les permissions :

```bash
# Vérifier le statut de SELinux
sestatus

# Autoriser le port de l'application
sudo semanage port -a -t http_port_t -p tcp 8089

# Si nécessaire, ajuster les contextes
sudo chcon -R -t bin_t /opt/ultimate-kea-dashboard/bin/
sudo chcon -R -t lib_t /opt/ultimate-kea-dashboard/lib/
```

En cas de problèmes, vérifiez les logs SELinux :

```bash
sudo ausearch -m avc -ts recent | grep ultimate-dashboard
```

## Certificats SSL

Sur Fedora, les certificats SSL se trouvent dans :

```bash
# Certificats par défaut
/etc/pki/tls/certs/localhost.crt
/etc/pki/tls/private/localhost.key
```

Pour générer vos propres certificats auto-signés :

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/pki/tls/private/dashboard.key \
  -out /etc/pki/tls/certs/dashboard.crt
```

Puis dans `/etc/ultimate-dashboard/ultimate-dashboard.conf` :

```ini
ssl_enabled = true
ssl_cert = /etc/pki/tls/certs/dashboard.crt
ssl_key = /etc/pki/tls/private/dashboard.key
```

## Service systemd

### Créer le service

Le fichier est créé automatiquement dans `/etc/systemd/system/ultimate-dashboard.service`.

Contenu type :

```ini
[Unit]
Description=Ultimate Kea DHCP Dashboard
After=network.target kea-dhcp4.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ultimate-kea-dashboard
ExecStart=/usr/bin/python3 /opt/ultimate-kea-dashboard/bin/ultimate-dashboard
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

# Arrêter
sudo systemctl stop ultimate-dashboard
```

## Configuration de Kea DHCP

### Emplacement des fichiers Kea

```bash
# Configuration
/etc/kea/kea-dhcp4.conf

# Leases
/var/lib/kea/kea-leases4.csv

# Socket de contrôle
/run/kea/kea4-ctrl-socket
```

### Activer le socket de contrôle Kea

Éditez `/etc/kea/kea-dhcp4.conf` :

```json
{
  "Dhcp4": {
    "control-socket": {
      "socket-type": "unix",
      "socket-name": "/run/kea/kea4-ctrl-socket"
    }
  }
}
```

Redémarrez Kea :

```bash
sudo systemctl restart kea-dhcp4
```

## Dépannage

### Le service ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u ultimate-dashboard -n 50

# Vérifier les permissions
ls -la /opt/ultimate-kea-dashboard/

# Tester manuellement
sudo python3 /opt/ultimate-kea-dashboard/bin/ultimate-dashboard
```

### Problèmes de permission

```bash
# Vérifier SELinux
sudo ausearch -m avc -ts recent

# Temporairement en mode permissif (pour debug)
sudo setenforce 0

# Revenir en mode enforcing
sudo setenforce 1
```

### Erreurs de réseau

```bash
# Vérifier le port
sudo netstat -tulpn | grep 8089

# Vérifier le pare-feu
sudo firewall-cmd --list-all
```

### Python ou dépendances manquantes

```bash
# Vérifier Python
python3 --version

# Réinstaller les dépendances
sudo dnf reinstall python3 python3-pip nmap iputils
```

## Mise à jour

```bash
cd ultimate-kea-dashboard
git pull
sudo bash install.sh
sudo systemctl restart ultimate-dashboard
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
```

## Support

Pour plus d'informations : https://github.com/NeySlim/ultimate-kea-dashboard/issues
