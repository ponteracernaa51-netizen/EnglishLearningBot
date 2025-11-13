from telegram import Update, CallbackQuery, constants
from telegram.ext import ContextTypes
import config
import database
import keyboards
from utils.languages import get_text
from handlers.topic_handler import back_to_topics

async def send_new_phrase(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE) -> int:
    await query.answer()

    lang_code = context.user_data.get('lang', 'en')
    topic = context.user_data.get('topic')
    difficulty = context.user_data.get('difficulty')
    source_lang = context.user_data.get('source_lang')
    target_lang = context.user_data.get('target_lang')

    if not all([lang_code, topic, difficulty, source_lang, target_lang]):
        await query.edit_message_text(
            text="Xatolik yuz berdi. Iltimos, mavzuni qaytadan tanlang.",
            reply_markup=keyboards.get_topics_keyboard(lang_code or 'uz')
        )
        return config.SELECTING_TOPIC

    phrase_data = await database.get_random_phrase(topic, difficulty)

    if not phrase_data:
        error_text = get_text(lang_code, 'error_no_phrase')
        choose_topic_text = get_text(lang_code, 'choose_topic')
        await query.edit_message_text(
            text=f"{error_text}\n\n{choose_topic_text}",
            reply_markup=keyboards.get_topics_keyboard(lang_code)
        )
        return config.SELECTING_TOPIC

    original_phrase = phrase_data.get(f'phrase_{source_lang}')
    correct_translation = phrase_data.get(f'phrase_{target_lang}')

    context.user_data['original_phrase'] = original_phrase
    context.user_data['correct_translation'] = correct_translation

    lang_name = get_text(lang_code, f'lang_name_{target_lang}')
    text_to_send = get_text(lang_code, 'translate_phrase_to').format(
        lang_name=lang_name,
        phrase=original_phrase
    )

    await query.edit_message_text(
        text=text_to_send,
        parse_mode=constants.ParseMode.HTML
    )

    return config.AWAITING_TRANSLATION

async def select_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    parts = query.data.split('_')
    if len(parts) < 2:
        await query.answer("Xatolik: noto‘g‘ri formatdagi tugma!", show_alert=True)
        return config.SELECTING_DIFFICULTY

    difficulty = parts[1]
    context.user_data['difficulty'] = difficulty
    lang_code = context.user_data.get('lang', 'en')

    await query.edit_message_text(
        text=get_text(lang_code, 'choose_direction'),
        reply_markup=keyboards.get_direction_keyboard(lang_code)
    )
    return config.SELECTING_DIRECTION

async def select_direction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    direction_parts = query.data.split('_')
    if len(direction_parts) < 3:
        await query.answer("Xatolik: noto‘g‘ri formatdagi tugma!", show_alert=True)
        return config.SELECTING_DIRECTION

    source_lang, target_lang = direction_parts[1], direction_parts[2]
    context.user_data['source_lang'] = source_lang
    context.user_data['target_lang'] = target_lang

    return await send_new_phrase(query, context)