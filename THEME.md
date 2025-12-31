# Thème Garuda Linux Mokka

Le dashboard utilise maintenant un thème inspiré de Garuda Linux Mokka, avec des tons sombres élégants et des accents dorés/orangés.

## Palette de couleurs

### Couleurs principales
- **Background**: `#1a1515` → `#2d2424` (gradient marron foncé)
- **Surface**: `rgba(45, 36, 36, 0.6)` (tableaux semi-transparents)
- **Texte primaire**: `#e5e9f0` (blanc cassé)
- **Texte secondaire**: `#d8dee9` (gris clair)

### Accents
- **Primary**: `#d08770` (orange/saumon)
- **Accent**: `#ebcb8b` (doré)
- **Success**: `#a3be8c` (vert)
- **Error**: `#bf616a` (rouge)
- **Info**: `#88c0d0` (bleu clair)

## Caractéristiques du design

### Effets visuels
- ✨ Dégradés subtils sur les titres
- ✨ Ombres profondes (box-shadow)
- ✨ Bordures colorées sur les lignes actives/inactives
- ✨ Transparence élégante (rgba)
- ✨ Scrollbar personnalisée (orange #d08770)
- ✨ Transitions fluides au survol

### Typographie
- **Font**: Segoe UI, Tahoma
- **H1**: 2.5em, gradient doré→orange
- **H2**: 1.5em, orange #d08770, uppercase
- **Headers tableau**: uppercase + letter-spacing

### Éléments interactifs
- **Hover tableaux**: fond marron plus clair `#3d3030`
- **Hover headers**: gradient accentué
- **Liens**: `#88c0d0` → `#ebcb8b` au survol
- **Puces**: `▸` en orange #d08770

## Statuts de scan

- 🟨 **Scan en cours**: `#ebcb8b` (doré)
- 🟩 **Prochain scan**: `#a3be8c` (vert)
- 🟦 **En attente**: `#88c0d0` (bleu)
- ⬜ **Jamais scanné**: `#666` (gris)

## États des baux

- 🟩 **Actif**: Fond vert subtil + bordure gauche verte `#a3be8c`
- 🟥 **Inactif**: Fond rouge subtil + bordure gauche rouge `#bf616a`

## Accès

Le thème est visible sur: http://localhost:8089

## Favicon

Le dashboard utilise un favicon SVG vectoriel intégré au thème Mokka.

### Design
- **Format**: SVG inline (data URI)
- **Taille**: 100x100px (vectoriel, adaptable)
- **Poids**: ~1KB

### Symbolisme
- 🔶 **Serveur central**: Gradient doré→orange (#ebcb8b → #d08770)
- 🟢 **Clients actifs**: 3 cercles verts (#a3be8c)
- 🟦 **Clients info**: 3 cercles bleus (#88c0d0)
- 🟫 **Background**: Marron foncé (#1a1515)
- ━━ **Connexions**: Lignes représentant le réseau DHCP

### Fichiers
- Inline: Intégré dans le HTML du dashboard
- Source: `/opt/ultimate-dashboard/data/favicon.svg`

Le favicon représente visuellement un serveur DHCP (en haut) connecté à plusieurs clients (en bas) via un réseau.
