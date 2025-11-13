import logging
import json
from telegram import Update
from telegram.ext import ContextTypes
import ai_checker
import config
import keyboards
import database
from utils.languages import get_text
from handlers.difficulty_handler import send_new_phrase

logger = logging.getLogger(__name__)

async def handle_translation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang_code = context.user_data.get('lang', 'en')
    await update.message.reply_text(get_text(lang_code, 'checking'))

    feedback_json_str = await ai_checker.check_translation(
        original_phrase=context.user_data['original_phrase'],
        user_translation=update.message.text,
        source_lang=context.user_data['source_lang'],
        target_lang=context.user_data['target_lang'],
        ui_lang=lang_code
    )

    try:
        feedback_data = json.loads(feedback_json_str)

        if 'error' in feedback_data:
            formatted_response = feedback_data['error']
        else:
            score = feedback_data.get('score')
            corrected = feedback_data.get('corrected_translation')
            explanation = feedback_data.get('explanation')

            if score is not None:
                await database.update_user_stats(update.message.from_user.id, int(score))

            formatted_response = (
                f"**📊 Оценка**: {score}/10\n\n"
                f"**✅ Правильный вариант**: `{corrected}`\n\n"
                f"**💡 Пояснение**: {explanation}"
            )

    except (json.JSONDecodeError, TypeError):
        logger.warning(f"Не удалось распарсить JSON от AI: {feedback_json_str}")
        formatted_response = "Не удалось обработать ответ от сервиса проверки. Попробуйте следующую фразу."

    await update.message.reply_text(
        text=formatted_response,
        reply_markup=keyboards.get_next_action_keyboard(lang_code),
        parse_mode='Markdown'
    )
    return config.AWAITING_TRANSLATION

async def next_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    return await send_new_phrase(query, context)