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

# Словарь переводов для шаблона
LABELS = {
    'en': {
        'score': 'Score',
        'correct': 'Correct',
        'explanation': 'Explanation',
        'continue': 'Continue!'
    },
    'ru': {
        'score': 'Оценка',
        'correct': 'Правильный вариант',
        'explanation': 'Пояснение',
        'continue': 'Продолжай!'
    },
    'uz': {
        'score': 'Baho',
        'correct': "To'g'ri",
        'explanation': 'Izoh',
        'continue': "Davom et!"
    }
}


async def handle_translation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    lang_code: str = context.user_data.get('lang', 'en')
    labels = LABELS.get(lang_code, LABELS['en'])
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
            await update.message.reply_text(feedback['error'])
        else:
            score: Optional[int] = feedback.get('score')
            corrected: str = feedback.get('corrected_translation', '')
            explanation: str = feedback.get('explanation', '')
            
            if isinstance(score, int):
                await database.update_user_stats(update.message.from_user.id, score)
            
            formatted = (
                f"📊 Score: 📊 {labels['score']}: {score}/10\n"
                f"✅ {labels['correct']}: \"{corrected}\"\n"
                f"💡 {labels['explanation']}: {explanation}\n"
            )
            await update.message.reply_text(formatted)
        
        # Всегда отправляем новую фразу после feedback
        await _send_next_with_prompt(update, context, lang_code, labels)
        return config.AWAITING_TRANSLATION
        
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Не удалось распарсить JSON от AI: {feedback_json}. Ошибка: {e}")
        await update.message.reply_text("Не удалось обработать ответ от сервиса проверки.")
        await _send_next_with_prompt(update, context, lang_code, labels)
        return config.AWAITING_TRANSLATION


async def _send_next_with_prompt(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    lang_code: str,
    labels: dict,
) -> None:
    """Отправляет новую фразу и сообщение с 'Продолжай!'."""
    # send_new_phrase отправит фразу сам; fallback для query
    query = update.callback_query
    await send_new_phrase(query, context)  # Если query None, доработай send_new_phrase для update
    
    # Отдельное сообщение с продолжением и кнопками (как в примере)
    continue_text = f"{labels['continue']}"
    await update.message.reply_text(
        continue_text,
        reply_markup=keyboards.get_next_action_keyboard(lang_code)
    )


async def next_phrase(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    return await send_new_phrase(update.callback_query, context)
