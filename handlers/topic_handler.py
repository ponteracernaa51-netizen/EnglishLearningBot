from telegram import Update
from telegram.ext import ContextTypes
import keyboards
import config
from utils.languages import get_text

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    lang_code = query.data.split('_')[1]
    context.user_data['lang'] = lang_code

    await query.edit_message_text(
        text=f"{get_text(lang_code, 'language_selected')}\n\n{get_text(lang_code, 'choose_topic')}",
        reply_markup=keyboards.get_topics_keyboard(lang_code)
    )
    return config.SELECTING_TOPIC

async def select_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    topic = query.data.replace('topic_', '', 1)

    context.user_data['topic'] = topic
    lang_code = context.user_data['lang']

    await query.edit_message_text(
        text=get_text(lang_code, 'choose_difficulty'),
        reply_markup=keyboards.get_difficulty_keyboard(lang_code)
    )
    return config.SELECTING_DIFFICULTY

async def back_to_topics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query if hasattr(update, 'callback_query') else update
    
    await query.answer()
    lang_code = context.user_data.get('lang', 'en') 
    await query.edit_message_text(
        text=get_text(lang_code, 'choose_topic'),
        reply_markup=keyboards.get_topics_keyboard(lang_code)
    )
    return config.SELECTING_TOPIC