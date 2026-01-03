# Support Multi-Distribution

> **Languages / Langues:** 🇬🇧 [English](README-MULTIDISTRO.en.md) _(in progress)_ | 🇫🇷 [Français](README-MULTIDISTRO.md)

---

Ultimate Kea DHCP Dashboard est maintenant compatible avec les principales distributions Linux !

## 🎯 Distributions Supportées

### 🔵 Debian et dérivés
- Debian 10+
- Ubuntu 20.04+
- Linux Mint 20+
- Pop!_OS 20.04+

### 🔴 Red Hat et dérivés
- Fedora 35+
- CentOS 8+
- RHEL 8+
- Rocky Linux 8+
- AlmaLinux 8+

### 💠 Arch et dérivés
- Arch Linux
- Manjaro
- EndeavourOS

### 🟢 SUSE et dérivés
- openSUSE Leap 15.3+
- openSUSE Tumbleweed
- SLES 15+

## 🚀 Installation Rapide

L'installateur détecte automatiquement votre distribution :

```bash
# Télécharger et exécuter
curl -sL https://raw.githubusercontent.com/username/ultimate-kea-dhcp-dashboard/main/install.sh -o install.sh
sudo bash install.sh
```

C'est tout ! L'installateur :
1. ✅ Détecte votre distribution Linux
2. ✅ Utilise le bon gestionnaire de paquets
3. ✅ Installe les bonnes dépendances
4. ✅ Configure les chemins SSL adaptés
5. ✅ Crée le service systemd
6. ✅ Démarre le dashboard

## 📚 Guides Spécifiques

Des guides détaillés sont disponibles pour chaque famille de distributions :

- **Fedora/CentOS/RHEL** → [docs/INSTALL-FEDORA.md](INSTALL-FEDORA.md)
  - Configuration SELinux
  - Pare-feu firewalld
  - Activation EPEL

- **Arch/Manjaro** → [docs/INSTALL-ARCH.md](INSTALL-ARCH.md)
  - Installation via Pacman
  - Configuration nftables
  - Optimisations spécifiques

- **Toutes les distributions** → [docs/DISTRIBUTIONS.md](DISTRIBUTIONS.md)
  - Matrice de compatibilité
  - Commandes par distribution
  - Dépannage général

## 🔧 Que Fait l'Installateur ?

### Détection Automatique

```bash
# L'installateur lit /etc/os-release
Distribution: Fedora Linux 39
Gestionnaire de paquets: DNF
```

### Installation des Dépendances

Selon votre distribution, l'installateur utilise :

| Distribution | Commande |
|--------------|----------|
| Debian/Ubuntu | `apt-get install nmap arping python3 python3-pip` |
| Fedora | `dnf install nmap iputils python3 python3-pip` |
| CentOS/RHEL | `dnf install epel-release && dnf install ...` |
| Arch | `pacman -S nmap iputils python python-pip` |
| openSUSE | `zypper install nmap iputils python3 python3-pip` |

### Configuration SSL

Les chemins de certificats sont adaptés automatiquement :

| Distribution | Certificat | Clé |
|--------------|------------|-----|
| Debian/Ubuntu | `/etc/ssl/certs/ssl-cert-snakeoil.pem` | `/etc/ssl/private/ssl-cert-snakeoil.key` |
| Fedora/RHEL | `/etc/pki/tls/certs/localhost.crt` | `/etc/pki/tls/private/localhost.key` |

## 🔥 Configuration du Pare-feu

### Debian/Ubuntu (UFW)
```bash
sudo ufw allow 8089/tcp
sudo ufw reload
```

### Fedora/RHEL/CentOS (firewalld)
```bash
sudo firewall-cmd --permanent --add-port=8089/tcp
sudo firewall-cmd --reload
```

### Arch (nftables)
```bash
# Éditer /etc/nftables.conf
sudo nano /etc/nftables.conf
# Ajouter : tcp dport 8089 accept
sudo systemctl restart nftables
```

## 🛡️ SELinux (RHEL/CentOS/Fedora)

Si SELinux est activé :

```bash
# Autoriser le port
sudo semanage port -a -t http_port_t -p tcp 8089

# Vérifier les erreurs
sudo ausearch -m avc -ts recent | grep ultimate-dashboard
```

## ✅ Vérification

Après l'installation :

```bash
# Statut du service
sudo systemctl status ultimate-dashboard

# Logs en temps réel
sudo journalctl -u ultimate-dashboard -f

# Test d'accès
curl http://localhost:8089
```

## 🐛 Dépannage Rapide

### Le service ne démarre pas
```bash
# Voir les erreurs
sudo journalctl -u ultimate-dashboard -n 50 --no-pager

# Tester manuellement
sudo python3 /opt/ukd/bin/ultimate-dashboard
```

### Python manquant
```bash
# Debian/Ubuntu
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

### Port déjà utilisé
```bash
# Trouver le processus
sudo lsof -i :8089

# Modifier le port dans la config
sudo nano /etc/ultimate-dashboard/ultimate-dashboard.conf
# port = 8090

# Redémarrer
sudo systemctl restart ultimate-dashboard
```

## 📖 Documentation Complète

- [README principal](../README.md) - Vue d'ensemble et fonctionnalités
- [DISTRIBUTIONS.md](DISTRIBUTIONS.md) - Matrice de compatibilité détaillée
- [INSTALL-FEDORA.md](INSTALL-FEDORA.md) - Guide Fedora/RHEL/CentOS
- [INSTALL-ARCH.md](INSTALL-ARCH.md) - Guide Arch/Manjaro
- [MULTI-DISTRO-DEV.md](MULTI-DISTRO-DEV.md) - Ajouter une distribution

## 💡 Commandes Utiles par Distribution

### Debian/Ubuntu
```bash
# Mise à jour système
sudo apt update && sudo apt upgrade

# Réinstaller les dépendances
sudo apt install --reinstall nmap arping python3 python3-pip

# Logs système
sudo journalctl -xe
```

### Fedora/RHEL/CentOS
```bash
# Mise à jour système
sudo dnf update

# Activer EPEL (CentOS/RHEL)
sudo dnf install epel-release

# Vérifier SELinux
sestatus
```

### Arch/Manjaro
```bash
# Mise à jour système
sudo pacman -Syu

# Rechercher un paquet
pacman -Ss keyword

# Informations sur un paquet
pacman -Si package_name
```

## 🤝 Contribution

Votre distribution n'est pas supportée ? Contribuez !

1. Testez l'installateur sur votre distribution
2. Consultez [MULTI-DISTRO-DEV.md](MULTI-DISTRO-DEV.md)
3. Soumettez une Pull Request avec les adaptations nécessaires

## 📞 Support

- **Issues GitHub** : https://github.com/username/ultimate-kea-dashboard/issues
- **Documentation** : Voir les guides dans `docs/`
- **Tests** : Utilisez `test-distro-detection.sh` pour vérifier la détection

## 📜 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](../LICENSE) pour plus de détails.

---

**Version** : 1.2.0  
**Distributions testées** : Debian 11+, Ubuntu 20.04+, Fedora 35+, Arch Linux  
**Mise à jour** : 2026-01-01
