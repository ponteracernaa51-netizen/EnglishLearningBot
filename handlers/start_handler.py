from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import keyboards
import config
from utils.languages import get_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает диалог, предлагает выбрать язык."""
    context.user_data.clear()
    # Приветствие на всех языках для первого контакта
    welcome_text = (
        f"{get_text('ru', 'welcome')}\n\n"
        f"{get_text('uz', 'welcome')}\n\n"
        f"{get_text('en', 'welcome')}"
    )
    await update.message.reply_text(
        text=welcome_text,
        reply_markup=keyboards.get_language_keyboard()
    )
    return config.SELECTING_LANG

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Прерывает диалог."""
    await update.message.reply_text("Диалог завершен. Введите /start, чтобы начать заново.")
    context.user_data.clear()
    return ConversationHandler.END