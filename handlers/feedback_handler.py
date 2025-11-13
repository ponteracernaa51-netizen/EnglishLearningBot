import logging
import json
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
import ai_checker
import config
import keyboards
import database
from utils.languages import get_text
from handlers.difficulty_handler import send_new_phrase

logger = logging.getLogger(__name__)


async def handle_translation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    lang_code: str = context.user_data.get('lang', 'en')
    await update.message.reply_text(get_text(lang_code, 'checking'))
    
    user_data = context.user_data
    feedback_json = await ai_checker.check_translation(
        original_phrase=user_data['original_phrase'],
        user_translation=update.message.text,
        source_lang=user_data['source_lang'],
        target_lang=user_data['target_lang'],
        ui_lang=lang_code,
    )
    
    try:
        feedback = json.loads(feedback_json)
        
        if 'error' in feedback:
            formatted = feedback['error']
        else:
            score: Optional[int] = feedback.get('score')
            corrected: str = feedback.get('corrected_translation', '')
            explanation: str = feedback.get('explanation', '')
            
            if score is not None:
                await database.update_user_stats(update.message.from_user.id, score)
            
            formatted = (
                f"**📊 Оценка**: {score}/10\n\n"
                f"**✅ Правильный вариант**: `{corrected}`\n\n"
                f"**💡 Пояснение**: {explanation}"
            )
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Не удалось распарсить JSON от AI: {feedback_json}. Ошибка: {e}")
        formatted = "Не удалось обработать ответ от сервиса проверки. Попробуйте следующую фразу."
    
    await update.message.reply_text(
        text=formatted,
        reply_markup=keyboards.get_next_action_keyboard(lang_code),
        parse_mode='Markdown',
    )
    return config.AWAITING_TRANSLATION


async def next_phrase(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    return await send_new_phrase(update.callback_query, context)
