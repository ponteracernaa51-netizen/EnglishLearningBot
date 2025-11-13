from typing import Optional
from telegram import Update, CallbackQuery, constants
from telegram.ext import ContextTypes
import config
import database
import keyboards
from utils.languages import get_text
from handlers.topic_handler import back_to_topics


async def send_new_phrase(
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    await query.answer()
    lang_code: str = context.user_data.get('lang', 'en')
    topic: Optional[str] = context.user_data.get('topic')
    difficulty: Optional[str] = context.user_data.get('difficulty')
    source_lang: Optional[str] = context.user_data.get('source_lang')
    target_lang: Optional[str] = context.user_data.get('target_lang')
    
    if not all([topic, difficulty, source_lang, target_lang]):
        await query.edit_message_text(
            text=get_text(lang_code, 'error_incomplete_setup'),
            reply_markup=keyboards.get_topics_keyboard(lang_code)
        )
        return config.SELECTING_TOPIC
    
    phrase_data = await database.get_random_phrase(topic, difficulty)
    if not phrase_data:
        await query.edit_message_text(
            text=f"{get_text(lang_code, 'error_no_phrase')}\n\n{get_text(lang_code, 'choose_topic')}",
            reply_markup=keyboards.get_topics_keyboard(lang_code)
        )
        return config.SELECTING_TOPIC
    
    original_phrase: str = phrase_data[f'phrase_{source_lang}']
    correct_translation: str = phrase_data[f'phrase_{target_lang}']
    context.user_data.update({
        'original_phrase': original_phrase,
        'correct_translation': correct_translation
    })
    
    lang_name: str = get_text(lang_code, f'lang_name_{target_lang}')
    text_to_send: str = get_text(lang_code, 'translate_phrase_to').format(
        lang_name=lang_name, phrase=original_phrase
    )
    
    await query.edit_message_text(
        text=text_to_send,
        parse_mode=constants.ParseMode.HTML
    )
    return config.AWAITING_TRANSLATION


async def select_difficulty(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    query: CallbackQuery = update.callback_query
    await query.answer()
    
    parts: list[str] = query.data.split('_')
    if len(parts) < 2:
        await query.answer("Xatolik: noto'g'ri formatdagi tugma!", show_alert=True)
        return config.SELECTING_DIFFICULTY
    
    context.user_data['difficulty'] = parts[1]
    lang_code: str = context.user_data.get('lang', 'en')
    
    await query.edit_message_text(
        text=get_text(lang_code, 'choose_direction'),
        reply_markup=keyboards.get_direction_keyboard(lang_code)
    )
    return config.SELECTING_DIRECTION


async def select_direction(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    query: CallbackQuery = update.callback_query
    await query.answer()
    
    direction_parts: list[str] = query.data.split('_')
    if len(direction_parts) < 3:
        await query.answer("Xatolik: noto'g'ri formatdagi tugma!", show_alert=True)
        return config.SELECTING_DIRECTION
    
    source_lang: str = direction_parts[1]
    target_lang: str = direction_parts[2]
    context.user_data.update({
        'source_lang': source_lang,
        'target_lang': target_lang
    })
    
    return await send_new_phrase(query, context)
