# PEP 668 et Gestion des Packages Python

## Contexte

**PEP 668** (Marking Python base environments as "externally managed") est une spécification Python qui protège l'environnement Python système contre les modifications non intentionnelles par pip.

## Distributions Affectées

### Avec PEP 668 Activé
- **Debian 12+** (Bookworm)
- **Ubuntu 23.04+** (Lunar et suivants)
- **Fedora 38+**
- Autres distributions modernes avec Python 3.11+

### Comportement
```bash
$ pip3 install psutil
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
```

## Solution Adoptée par Ultimate Kea Dashboard

### ✅ Utilisation des Packages Système (Recommandé)

Au lieu d'utiliser `pip install`, nous utilisons les gestionnaires de paquets système :

| Distribution | Commande |
|--------------|----------|
| Debian/Ubuntu | `apt install python3-psutil` |
| Fedora/RHEL/CentOS | `dnf install python3-psutil` |
| Arch/Manjaro | `pacman -S python-psutil` |
| openSUSE | `zypper install python3-psutil` |

### Avantages

1. **Compatibilité PEP 668** : Pas de conflit avec la protection système
2. **Mises à jour automatiques** : Via le gestionnaire de paquets
3. **Intégration système** : Cohérence avec les autres packages
4. **Stabilité** : Versions testées pour la distribution
5. **Sécurité** : Correctifs de sécurité via les dépôts officiels
6. **SELinux compatible** : Contextes corrects automatiquement

## Alternatives (Non Recommandées pour Production)

### Option 1 : --break-system-packages

```bash
pip3 install --break-system-packages psutil
```

**Inconvénients** :
- ❌ Contourne les protections système
- ❌ Risque de conflit avec packages système
- ❌ Mises à jour manuelles nécessaires
- ❌ Problèmes potentiels avec SELinux

### Option 2 : --user

```bash
pip3 install --user psutil
```

**Inconvénients** :
- ❌ Installation par utilisateur (pas système)
- ❌ Ne fonctionne pas pour les services systemd en root
- ❌ Chemins différents (~/.local/lib)

### Option 3 : Environnement Virtuel

```bash
python3 -m venv /opt/ukd/venv
source /opt/ukd/venv/bin/activate
pip install psutil
```

**Inconvénients** :
- ❌ Complexité accrue pour systemd
- ❌ Nécessite modification du service
- ❌ Plus de maintenance
- ✅ OK pour développement uniquement

## Disponibilité de psutil

### Tous les Packages Système Disponibles

| Distribution | Package | Dépôt |
|--------------|---------|-------|
| Debian 10+ | python3-psutil | main |
| Ubuntu 20.04+ | python3-psutil | universe |
| Fedora 35+ | python3-psutil | fedora |
| RHEL/CentOS 8+ | python3-psutil | EPEL |
| Rocky/Alma 8+ | python3-psutil | EPEL |
| Arch Linux | python-psutil | extra |
| Manjaro | python-psutil | extra |
| openSUSE Leap | python3-psutil | oss |
| openSUSE TW | python3-psutil | oss |

**Conclusion** : psutil est disponible dans **tous** les dépôts officiels !

## Implémentation dans l'Installateur

### install.sh

```bash
case "$PKG_MANAGER" in
    apt)
        apt install python3-psutil
        ;;
    dnf|yum)
        dnf install python3-psutil  # Via EPEL si nécessaire
        ;;
    pacman)
        pacman -S python-psutil
        ;;
    zypper)
        zypper install python3-psutil
        ;;
esac
```

### Aucun Appel à pip

L'installateur n'utilise **jamais** pip pour installer psutil. Tout passe par les gestionnaires système.

## Autres Dépendances Python

### Bibliothèques Standard Uniquement

Ultimate Kea Dashboard utilise **uniquement** :
- Bibliothèques Python standard (json, http, socket, subprocess, etc.)
- **psutil** (seule dépendance externe)

Aucune autre bibliothèque tierce n'est nécessaire.

## Pour les Développeurs

### Environnement de Développement

Si vous développez le dashboard :

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Développer...

# Tester
python bin/ultimate-dashboard
```

### Production vs Développement

| Environnement | Méthode | Raison |
|---------------|---------|--------|
| Production | Packages système | Stabilité, sécurité, PEP 668 |
| Développement | venv + pip | Flexibilité, isolation |
| CI/CD | venv + pip | Reproductibilité |

## Migration depuis pip

Si vous avez installé psutil via pip :

### 1. Désinstaller pip version

```bash
pip3 uninstall psutil
# ou
pip3 uninstall --break-system-packages psutil
```

### 2. Installer version système

```bash
# Debian/Ubuntu
sudo apt install python3-psutil

# Fedora/RHEL/CentOS
sudo dnf install python3-psutil

# Arch
sudo pacman -S python-psutil

# openSUSE
sudo zypper install python3-psutil
```

### 3. Redémarrer le service

```bash
sudo systemctl restart ultimate-dashboard
```

## Vérification

### Check Installation

```bash
# Méthode 1 : Python
python3 -c "import psutil; print('psutil:', psutil.__version__)"

# Méthode 2 : Package système
# Debian/Ubuntu
dpkg -l | grep python3-psutil

# Fedora/RHEL
rpm -qa | grep python3-psutil

# Arch
pacman -Q python-psutil
```

### Check Source

```bash
# Afficher le chemin d'installation
python3 -c "import psutil; print(psutil.__file__)"

# Si dans /usr/lib/python3/dist-packages → Package système ✓
# Si dans /usr/local/lib → pip (à migrer)
# Si dans ~/.local/lib → pip --user (à migrer)
```

## Références

- [PEP 668](https://peps.python.org/pep-0668/) - Spécification officielle
- [Debian Python Policy](https://www.debian.org/doc/packaging-manuals/python-policy/)
- [Arch Python Guidelines](https://wiki.archlinux.org/title/Python)
- [psutil Documentation](https://psutil.readthedocs.io/)

## Résumé

✅ **DO** : Utiliser les packages système (python3-psutil, python-psutil)  
❌ **DON'T** : Utiliser pip en production  
✅ **DO** : Utiliser venv + pip pour développement  
❌ **DON'T** : Utiliser --break-system-packages en production  

Ultimate Kea Dashboard respecte ces bonnes pratiques et fonctionne parfaitement avec les packages système sur toutes les distributions supportées.
