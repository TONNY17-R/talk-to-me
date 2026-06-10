// Translation strings for different languages

export const translations = {
  en: {
    welcome: 'Welcome to Talk to Me',
    start_chat: 'Start Chatting',
    your_mental_health: 'Your Mental Health Support Platform',
    crisis_support: 'Crisis Support',
    assessments: 'Assessments',
    counselling: 'Professional Counselling',
    resources: 'Resources',
    logout: 'Logout',
    profile: 'Profile',
  },
  lg: {
    welcome: 'Tubiwayo ku Talk to Me',
    start_chat: 'Tandika okutegeeza',
    your_mental_health: 'Plateau Y\'Omutwe',
    crisis_support: 'Okukoma Okwa Kubuusabuusa',
    assessments: 'Okuwukiriza',
    counselling: 'Okwegendereza',
    resources: 'Obulamu',
    logout: 'Genda',
    profile: 'Essomeko',
  },
  sw: {
    welcome: 'Karibu kwa Talk to Me',
    start_chat: 'Anza Kuzungumza',
    your_mental_health: 'Jukumu Lako la Akili',
    crisis_support: 'Msaada wa Azma',
    assessments: 'Tathmini',
    counselling: 'Ushauri wa Kitaalum',
    resources: 'Rasilimali',
    logout: 'Toka Nje',
    profile: 'Wasifu',
  },
};

export const getTranslation = (key, language = 'en') => {
  return translations[language]?.[key] || translations.en[key];
};
