# Guide du Développeur - Support Multi-Distribution

Ce guide explique comment le support multi-distribution fonctionne et comment ajouter de nouvelles distributions.

## Architecture

Le système de support multi-distribution repose sur trois composants principaux :

### 1. Détection de la Distribution

La fonction `detect_distro()` dans `install.sh` détecte automatiquement la distribution Linux en cours d'exécution.

**Sources de détection** (par ordre de priorité) :
1. `/etc/os-release` - Standard moderne (systemd)
2. `/etc/redhat-release` - Systèmes Red Hat legacy
3. `/etc/debian_version` - Systèmes Debian legacy

**Variables définies** :
- `DISTRO` - ID de la distribution (ex: `ubuntu`, `fedora`, `arch`)
- `DISTRO_VERSION` - Version (ex: `22.04`, `38`)
- `DISTRO_NAME` - Nom complet (ex: `Ubuntu`, `Fedora Linux`)
- `PKG_MANAGER` - Gestionnaire de paquets (ex: `apt`, `dnf`, `pacman`)
- `PKG_UPDATE` - Commande de mise à jour
- `PKG_INSTALL` - Commande d'installation

### 2. Abstraction du Gestionnaire de Paquets

Chaque distribution utilise un gestionnaire de paquets différent :

| Distribution | Gestionnaire | Update | Install |
|--------------|--------------|--------|---------|
| Debian/Ubuntu | APT | `apt-get update -qq` | `apt-get install -y -qq` |
| Fedora | DNF | `dnf check-update -q` | `dnf install -y -q` |
| CentOS/RHEL | DNF/YUM | `dnf/yum check-update -q` | `dnf/yum install -y -q` |
| Arch | Pacman | `pacman -Sy --noconfirm` | `pacman -S --noconfirm --needed` |
| openSUSE | Zypper | `zypper refresh -q` | `zypper install -y` |

### 3. Configurations Spécifiques

Certains paramètres varient selon la distribution :

#### Certificats SSL
```bash
# Debian/Ubuntu/Arch/openSUSE
/etc/ssl/certs/ssl-cert-snakeoil.pem
/etc/ssl/private/ssl-cert-snakeoil.key

# Fedora/RHEL/CentOS
/etc/pki/tls/certs/localhost.crt
/etc/pki/tls/private/localhost.key
```

#### Noms de paquets
| Paquet | Debian | Fedora | Arch |
|--------|--------|--------|------|
| ARP ping | `arping` | `iputils` | `iputils` |
| Python 3 | `python3` | `python3` | `python` |
| Python pip | `python3-pip` | `python3-pip` | `python-pip` |

## Ajouter une Nouvelle Distribution

### Étape 1 : Identifier la Distribution

Testez sur votre distribution cible :

```bash
# Afficher les informations
cat /etc/os-release

# Identifier l'ID
. /etc/os-release
echo $ID
```

### Étape 2 : Mettre à Jour detect_distro()

Dans `install.sh`, ajoutez votre distribution dans le bloc `case` :

```bash
detect_distro() {
    # ... code existant ...
    
    case "$DISTRO" in
        # ... distributions existantes ...
        
        votre_distro)
            PKG_MANAGER="nom_gestionnaire"
            PKG_UPDATE="commande_update"
            PKG_INSTALL="commande_install"
            ;;
            
        # ... suite du code ...
    esac
}
```

**Exemple pour Alpine Linux** :

```bash
alpine)
    PKG_MANAGER="apk"
    PKG_UPDATE="apk update"
    PKG_INSTALL="apk add --no-cache"
    ;;
```

### Étape 3 : Configurer les Dépendances

Dans `install_dependencies()`, ajoutez les noms de paquets spécifiques :

```bash
install_dependencies() {
    # ... code existant ...
    
    case "$PKG_MANAGER" in
        # ... gestionnaires existants ...
        
        votre_gestionnaire)
            eval $PKG_INSTALL paquet1 paquet2 paquet3 >/dev/null 2>&1
            ;;
            
    esac
}
```

**Exemple Alpine** :

```bash
apk)
    eval $PKG_INSTALL nmap iputils python3 py3-pip >/dev/null 2>&1
    ;;
```

### Étape 4 : Configurer les Chemins SSL

Dans `get_default_ssl_paths()`, ajoutez les chemins par défaut :

```bash
get_default_ssl_paths() {
    case "$PKG_MANAGER" in
        # ... gestionnaires existants ...
        
        votre_gestionnaire)
            DEFAULT_SSL_CERT="/chemin/vers/cert.pem"
            DEFAULT_SSL_KEY="/chemin/vers/key.pem"
            ;;
            
    esac
}
```

### Étape 5 : Créer la Documentation

Créez un guide d'installation spécifique :

```bash
docs/INSTALL-VOTRE_DISTRO.md
```

Incluez :
- Instructions d'installation rapide
- Installation manuelle détaillée
- Configuration du pare-feu
- Particularités de la distribution
- Dépannage spécifique

Utilisez `docs/INSTALL-FEDORA.md` ou `docs/INSTALL-ARCH.md` comme modèle.

### Étape 6 : Mettre à Jour la Documentation Générale

1. **docs/DISTRIBUTIONS.md** :
   - Ajoutez la distribution dans la liste
   - Documentez le gestionnaire de paquets
   - Indiquez les dépendances

2. **README.md** :
   - Ajoutez dans la section "Supported Distributions"
   - Ajoutez l'exemple d'installation manuelle

3. **CHANGELOG.md** :
   - Documentez l'ajout de la nouvelle distribution

### Étape 7 : Tester

Tests essentiels :

```bash
# 1. Vérifier la syntaxe
bash -n install.sh

# 2. Tester la détection
bash -c 'source install.sh; detect_distro; echo "Distro: $DISTRO, Manager: $PKG_MANAGER"'

# 3. Installation complète sur VM
sudo bash install.sh

# 4. Vérifier le service
sudo systemctl status ultimate-dashboard

# 5. Accès web
curl http://localhost:8089
```

## Particularités par Type de Distribution

### Distributions Basées sur Debian
- Utilisent APT
- Fichiers de configuration dans `/etc`
- Logs avec journalctl
- Certificats dans `/etc/ssl`

### Distributions Basées sur Red Hat
- Utilisent DNF ou YUM
- **Important** : Activer EPEL pour certains paquets
- Certificats dans `/etc/pki/tls`
- SELinux activé par défaut (à configurer)
- Firewalld comme pare-feu

### Distributions Rolling Release (Arch, etc.)
- Toujours à jour
- Paquets plus récents
- Nécessite `--needed` pour éviter la réinstallation
- Conventions de nommage parfois différentes (ex: `python` au lieu de `python3`)

### Distributions Entreprise (SLES, etc.)
- Cycles de release longs
- Stabilité prioritaire
- Support professionnel
- Certifications spécifiques

## Checklist de Validation

Avant de soumettre une PR pour une nouvelle distribution :

- [ ] La fonction `detect_distro()` identifie correctement la distribution
- [ ] Le gestionnaire de paquets correct est sélectionné
- [ ] Toutes les dépendances s'installent sans erreur
- [ ] Les chemins SSL par défaut sont corrects
- [ ] Le service systemd démarre correctement
- [ ] Le dashboard est accessible via le navigateur
- [ ] La documentation spécifique est créée
- [ ] Les exemples de pare-feu sont fournis
- [ ] Le CHANGELOG est mis à jour
- [ ] Les tests ont été effectués sur la distribution cible

## Cas Particuliers

### Distributions avec Plusieurs Versions de Python

```bash
# Arch (python = python3)
if [[ "$DISTRO" == "arch" ]]; then
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi
```

### Distributions avec SELinux

Ajoutez dans la documentation :

```bash
# Configurer SELinux
sudo semanage port -a -t http_port_t -p tcp 8089
```

### Distributions avec AppArmor

```bash
# Créer un profil AppArmor si nécessaire
sudo aa-complain /opt/ukd/bin/ultimate-dashboard
```

## Ressources

### Fichiers à Modifier
1. `install.sh` - Script d'installation principal
2. `docs/DISTRIBUTIONS.md` - Liste des distributions supportées
3. `docs/INSTALL-XXXX.md` - Guide spécifique (nouveau)
4. `README.md` - Documentation principale
5. `CHANGELOG.md` - Historique des changements

### Outils de Test

```bash
# Syntaxe Bash
bash -n install.sh
shellcheck install.sh

# Test en VM
# - VirtualBox
# - QEMU/KVM
# - Docker (attention aux limitations)
```

### Références

- [os-release specification](https://www.freedesktop.org/software/systemd/man/os-release.html)
- [Package manager comparison](https://wiki.archlinux.org/title/Pacman/Rosetta)
- [Systemd documentation](https://www.freedesktop.org/wiki/Software/systemd/)

## Support et Contribution

Pour ajouter une nouvelle distribution ou signaler un problème :
1. Ouvrez une issue sur GitHub
2. Fournissez les informations de votre distribution (`cat /etc/os-release`)
3. Décrivez les problèmes rencontrés
4. Proposez une PR avec les modifications nécessaires

## Maintien

Lors de chaque release :
- Tester sur au moins une distribution par famille
- Vérifier les changements de chemins/paquets
- Mettre à jour la documentation si nécessaire
- Valider les certificats SSL par défaut
