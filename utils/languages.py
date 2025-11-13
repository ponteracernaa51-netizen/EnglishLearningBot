# Словари для локализации интерфейса бота
TRANSLATIONS = {
    'ru': {
        'welcome': "👋 Здравствуйте! Я ваш бот для изучения английского. Пожалуйста, выберите язык интерфейса:",
        'language_selected': "🇷🇺 Язык изменен на Русский.",
        'choose_topic': "📚 Выберите тему для изучения:",
        'choose_difficulty': "📊 Выберите уровень сложности:",
        'translate_phrase_to': "✍️ Переведите эту фразу на **{lang_name}**:\n\n`{phrase}`",
        'checking': "⏳ Проверяю ваш перевод...",
        'next_phrase': "➡️ Следующая фраза",
        'change_topic': "⚙️ Сменить тему",
        'back_to_topics': "К темам",
        'error_no_phrase': "😕 Не удалось найти фразу по вашим критериям. Пожалуйста, выберите другую тему.",
        'lang_name_en': "английский", 'lang_name_ru': "русский", 'lang_name_uz': "узбекский",
    },
    'uz': {
        'welcome': "👋 Assalomu alaykum! Men sizning ingliz tilini o'rganish uchun botingizman. Iltimos, interfeys tilini tanlang:",
        'language_selected': "🇺🇿 Til O'zbek tiliga o'zgartirildi.",
        'choose_topic': "📚 O'rganish uchun mavzuni tanlang:",
        'choose_difficulty': "📊 Qiyinlik darajasini tanlang:",
        'translate_phrase_to': "✍️ Ushbu iborani **{lang_name}** tiliga tarjima qiling:\n\n`{phrase}`",
        'checking': "⏳ Tarjimangiz tekshirilmoqda...",
        'next_phrase': "➡️ Keyingi ibora",
        'change_topic': "⚙️ Mavzuni o'zgartirish",
        'back_to_topics': "Mavzularga",
        'error_no_phrase': "😕 Sizning mezonlaringiz bo'yicha ibora topilmadi. Iltimos, boshqa mavzu tanlang.",
        'lang_name_en': "ingliz", 'lang_name_ru': "rus", 'lang_name_uz': "o'zbek",
    },
    'en': {
        'welcome': "👋 Hello! I am your bot for learning English. Please choose the interface language:",
        'language_selected': "🇬🇧 Language changed to English.",
        'choose_topic': "📚 Choose a topic to study:",
        'choose_difficulty': "📊 Choose a difficulty level:",
        'translate_phrase_to': "✍️ Translate this phrase into **{lang_name}**:\n\n`{phrase}`",
        'checking': "⏳ Checking your translation...",
        'next_phrase': "➡️ Next phrase",
        'change_topic': "⚙️ Change topic",
        'back_to_topics': "Back to topics",
        'error_no_phrase': "😕 Could not find a phrase for your criteria. Please choose another topic.",
        'lang_name_en': "English", 'lang_name_ru': "Russian", 'lang_name_uz': "Uzbek",
    }
}


DIRECTION_NAMES = {
    'ru': {
        'ru_en': 'Русский 🇷🇺 → Английский 🇬🇧',
        'en_ru': 'Английский 🇬🇧 → Русский 🇷🇺',
        'uz_en': 'O‘zbek 🇺🇿 → Инглиз 🇬🇧',
        'en_uz': 'Инглиз 🇬🇧 → O‘zbek 🇺🇿',
    },
    'uz': {
        'ru_en': 'Ruscha 🇷🇺 → Inglizcha 🇬🇧',
        'en_ru': 'Inglizcha 🇬🇧 → Ruscha 🇷🇺',
        'uz_en': 'O‘zbek 🇺🇿 → Inglizcha 🇬🇧',
        'en_uz': 'Inglizcha 🇬🇧 → O‘zbek 🇺🇿',
    },
    'en': {
        'ru_en': 'Russian 🇷🇺 → English 🇬🇧',
        'en_ru': 'English 🇬🇧 → Russian 🇷🇺',
        'uz_en': 'Uzbek 🇺🇿 → English 🇬🇧',
        'en_uz': 'English 🇬🇧 → Uzbek 🇺🇿',
    }
}

TOPIC_NAMES = {
    'ru': {
        # Tenses
        'present_simple': 'Present Simple',
        'present_continuous': 'Present Continuous',
        'present_perfect': 'Present Perfect',
        'present_perfect_continuous': 'Present Perfect Continuous',
        'past_simple': 'Past Simple',
        'past_continuous': 'Past Continuous',
        'past_perfect': 'Past Perfect',
        'past_perfect_continuous': 'Past Perfect Continuous',
        'future_simple': 'Future Simple',
        'future_continuous': 'Future Continuous',
        'future_perfect': 'Future Perfect',
        'future_perfect_continuous': 'Future Perfect Continuous',

        # Grammar & Structure
        'passive_voice': 'Пассивный залог',
        'modal_verbs': 'Модальные глаголы',
        'conditionals': 'Условные предложения',
        'reported_speech': 'Косвенная речь',
        'questions_and_negatives': 'Вопросы и отрицания',
        'verb_to_be': 'Глагол "to be"',
        'irregular_verbs': 'Неправильные глаголы',
        'articles': 'Артикли',
        'prepositions': 'Предлоги',
        'comparatives_and_superlatives': 'Сравнительная и превосходная степень',
        'phrasal_verbs': 'Фразовые глаголы',

        # Everyday / Vocabulary Topics
        'travel': 'Путешествия',
        'food': 'Еда',
        'daily_routine': 'Ежедневная рутина',
        'shopping': 'Покупки',
        'weather': 'Погода',
        'hobbies': 'Хобби',
        'work': 'Работа',
        'health': 'Здоровье',
        'education': 'Образование',
        'technology': 'Технологии',
        'sports': 'Спорт',
        'entertainment': 'Развлечения',
        'family': 'Семья',
        'environment': 'Окружающая среда'
    },
    'uz': {
        # Tenses
        'present_simple': 'Present Simple',
        'present_continuous': 'Present Continuous',
        'present_perfect': 'Present Perfect',
        'present_perfect_continuous': 'Present Perfect Continuous',
        'past_simple': 'Past Simple',
        'past_continuous': 'Past Continuous',
        'past_perfect': 'Past Perfect',
        'past_perfect_continuous': 'Past Perfect Continuous',
        'future_simple': 'Future Simple',
        'future_continuous': 'Future Continuous',
        'future_perfect': 'Future Perfect',
        'future_perfect_continuous': 'Future Perfect Continuous',

        # Grammar & Structure
        'passive_voice': 'Passiv tovush',
        'modal_verbs': 'Modal fe\'llar',
        'conditionals': 'Shartli gaplar',
        'reported_speech': 'Bilvosita nutq',
        'questions_and_negatives': 'Savollar va inkor',
        'verb_to_be': '"To be" fe\'li',
        'irregular_verbs': 'Noto‘g‘ri fe\'llar',
        'articles': 'Maqolalar',
        'prepositions': 'Predloglar',
        'comparatives_and_superlatives': 'Taqqoslash va eng yuqori daraja',
        'phrasal_verbs': 'Frazal fe\'llar',

        # Everyday / Vocabulary Topics
        'travel': 'Sayohat',
        'food': 'Ovqat',
        'daily_routine': 'Kundalik odatlar',
        'shopping': 'Xarid qilish',
        'weather': 'Ob-havo',
        'hobbies': 'Sevimli mashg\'ulotlar',
        'work': 'Ish',
        'health': 'Salomatlik',
        'education': 'Ta\'lim',
        'technology': 'Texnologiya',
        'sports': 'Sport',
        'entertainment': 'Ko‘ngilochar',
        'family': 'Oila',
        'environment': 'Atrof-muhit'
    },
    'en': {
        # Tenses
        'present_simple': 'Present Simple',
        'present_continuous': 'Present Continuous',
        'present_perfect': 'Present Perfect',
        'present_perfect_continuous': 'Present Perfect Continuous',
        'past_simple': 'Past Simple',
        'past_continuous': 'Past Continuous',
        'past_perfect': 'Past Perfect',
        'past_perfect_continuous': 'Past Perfect Continuous',
        'future_simple': 'Future Simple',
        'future_continuous': 'Future Continuous',
        'future_perfect': 'Future Perfect',
        'future_perfect_continuous': 'Future Perfect Continuous',

        # Grammar & Structure
        'passive_voice': 'Passive Voice',
        'modal_verbs': 'Modal Verbs',
        'conditionals': 'Conditionals',
        'reported_speech': 'Reported Speech',
        'questions_and_negatives': 'Questions & Negatives',
        'verb_to_be': 'Verb "to be"',
        'irregular_verbs': 'Irregular Verbs',
        'articles': 'Articles',
        'prepositions': 'Prepositions',
        'comparatives_and_superlatives': 'Comparatives & Superlatives',
        'phrasal_verbs': 'Phrasal Verbs',

        # Everyday / Vocabulary Topics
        'travel': 'Travel',
        'food': 'Food',
        'daily_routine': 'Daily Routine',
        'shopping': 'Shopping',
        'weather': 'Weather',
        'hobbies': 'Hobbies',
        'work': 'Work',
        'health': 'Health',
        'education': 'Education',
        'technology': 'Technology',
        'sports': 'Sports',
        'entertainment': 'Entertainment',
        'family': 'Family',
        'environment': 'Environment'
    }
}

# Дополните переводы для всех времен...

DIFFICULTY_NAMES = {
    'ru': {'easy': 'Легкий', 'medium': 'Средний', 'hard': 'Сложный'},
    'uz': {'easy': 'Oson', 'medium': 'O\'rtacha', 'hard': 'Qiyin'},
    'en': {'easy': 'Easy', 'medium': 'Medium', 'hard': 'Hard'},
}


def get_text(lang_code: str, key: str) -> str:
    return TRANSLATIONS.get(lang_code, TRANSLATIONS['en']).get(key, f"_{key}_")

def get_topic_name(lang_code: str, key: str) -> str:
    # Возвращает английское название, если перевод не найден
    return TOPIC_NAMES.get(lang_code, TOPIC_NAMES['en']).get(key, key.replace('_', ' ').title())

def get_difficulty_name(lang_code: str, key: str) -> str:
    return DIFFICULTY_NAMES.get(lang_code, DIFFICULTY_NAMES['en']).get(key, key.title())
def get_direction_name(lang_code: str, key: str) -> str:
    """Получает локализованное название направления."""
    return DIRECTION_NAMES.get(lang_code, DIRECTION_NAMES['en']).get(key, key)