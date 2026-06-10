"""
Translation and localization utilities.
"""

TRANSLATIONS = {
    'en': {
        'welcome': 'Welcome to Talk to Me',
        'login_success': 'Login successful',
        'error_invalid_email': 'Invalid email format',
        'error_password_weak': 'Password is too weak',
        'crisis_support': 'If you are in crisis, please reach out to a mental health professional immediately',
        'appointment_booked': 'Your appointment has been booked',
        'session_started': 'Chat session started'
    },
    'lg': {
        'welcome': 'Karibu ku Talk to Me',
        'login_success': 'Okwewala',
        'error_invalid_email': 'Email si nono',
        'error_password_weak': 'Passowudi si wangu',
        'crisis_support': 'Singa oli mu mutwe guwa, ndegne kugana ne ssomo ly\'emmeeza',
        'appointment_booked': 'Okukuuma kwo kuteekeddweddwa',
        'session_started': 'Okukubaganya kwo kusuuddirira'
    },
    'sw': {
        'welcome': 'Karibu kwa Talk to Me',
        'login_success': 'Kuingia kumefanikiwa',
        'error_invalid_email': 'Barua pepe si sahihi',
        'error_password_weak': 'Nenosiri ni dhaifu',
        'crisis_support': 'Ikiwa uko katika azma, tafadhali wasiliana na mkunga wa akili',
        'appointment_booked': 'Miadi yako imeandaliwa',
        'session_started': 'Mazungumzo yameanza'
    }
}


def get_translation(key: str, language: str = 'en') -> str:
    """
    Get translated string.
    
    Args:
        key: Translation key
        language: Language code (en, lg, sw)
    
    Returns:
        Translated string or original key if not found
    """
    if language in TRANSLATIONS and key in TRANSLATIONS[language]:
        return TRANSLATIONS[language][key]
    elif key in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][key]
    else:
        return key


def add_translation(key: str, translations: dict) -> None:
    """Add new translations."""
    for language, text in translations.items():
        if language in TRANSLATIONS:
            TRANSLATIONS[language][key] = text


def get_available_languages() -> list:
    """Get list of available languages."""
    return list(TRANSLATIONS.keys())


def translate_assessment_results(results: dict, language: str = 'en') -> dict:
    """Translate assessment results."""
    risk_level_translations = {
        'en': {'low': 'Low', 'moderate': 'Moderate', 'high': 'High', 'critical': 'Critical'},
        'lg': {'low': 'Wabanga', 'moderate': 'Wakati', 'high': 'Wakyawa', 'critical': 'Wanzi nyo'},
        'sw': {'low': 'Chini', 'moderate': 'Kawaida', 'high': 'Juu', 'critical': 'Muhimu'}
    }
    
    if language in risk_level_translations:
        results['risk_level_text'] = risk_level_translations[language].get(
            results.get('risk_level'),
            results.get('risk_level')
        )
    
    return results
