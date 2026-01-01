"""
Translation module for Ultimate Kea Dashboard
Multi-language support (French, English, Spanish, German, Thai)
"""

import json
from pathlib import Path

# Load translations from JSON file
SCRIPT_DIR = Path(__file__).parent.parent.absolute()
TRANSLATIONS_FILE = SCRIPT_DIR / 'data' / 'translations.json'

# Load translations
TRANSLATIONS = {}
try:
    with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
        TRANSLATIONS = json.load(f)
except Exception as e:
    print(f"Error loading translations: {e}")
    # Fallback to minimal English translations
    TRANSLATIONS = {
        "en": {
            "title": "DHCP Dashboard",
            "error": "Translation file not found"
        }
    }


def get_translation(key, lang="fr"):
    """
    Get translation for a key in specified language
    
    Args:
        key: Translation key
        lang: Language code (fr, en, es, de, th)
    
    Returns:
        Translated string or key if not found
    """
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    # Fallback to French
    if key in TRANSLATIONS["fr"]:
        return TRANSLATIONS["fr"][key]
    # Return key itself if no translation found
    return key


def get_supported_languages():
    """Get list of supported language codes"""
    return list(TRANSLATIONS.keys())


def get_language_name(lang_code):
    """Get language name from code"""
    names = {
        "fr": "Français",
        "en": "English",
        "es": "Español",
        "de": "Deutsch",
        "th": "ไทย"
    }
    return names.get(lang_code, lang_code)
