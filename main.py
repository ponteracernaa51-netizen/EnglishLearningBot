# main.py

import logging
import asyncio
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import config
import database
from handlers import start_handler, topic_handler, difficulty_handler, feedback_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 8443))
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

app = Flask(__name__)

def setup_application() -> Application:
    if not config.TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN не найден!")

    application = (
        Application.builder()
        .token(config.TELEGRAM_TOKEN)
        .post_init(database.connect_db)
        .post_shutdown(database.close_db_pool)
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_handler.start)],
        states={
            config.SELECTING_LANG: [CallbackQueryHandler(topic_handler.select_language, pattern="^lang_")],
            config.SELECTING_TOPIC: [CallbackQueryHandler(topic_handler.select_topic, pattern="^topic_")],
            config.SELECTING_DIFFICULTY: [
                CallbackQueryHandler(difficulty_handler.select_difficulty, pattern="^difficulty_"),
                CallbackQueryHandler(topic_handler.back_to_topics, pattern="^back_to_topics$"),
            ],
            config.SELECTING_DIRECTION: [
                CallbackQueryHandler(difficulty_handler.select_direction, pattern="^direction_"),
                CallbackQueryHandler(topic_handler.back_to_topics, pattern="^back_to_topics$"),
            ],
            config.AWAITING_TRANSLATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_handler.handle_translation),
                CallbackQueryHandler(feedback_handler.next_phrase, pattern="^next_phrase$"),
                CallbackQueryHandler(topic_handler.back_to_topics, pattern="^change_topic$"),
            ],
        },
        fallbacks=[
            CommandHandler("start", start_handler.start),
            CommandHandler("cancel", start_handler.cancel)
        ],
    )
    application.add_handler(conv_handler)
    return application

ptb_app = setup_application()

@app.route("/")
def index():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
async def webhook():
    update_data = request.get_json()
    update = Update.de_json(update_data, ptb_app.bot)
    await ptb_app.process_update(update)
    return "OK", 200

# --- НОВЫЙ СЕКРЕТНЫЙ ЭНДПОИНТ ДЛЯ УСТАНОВКИ ВЕБХУКА ---
@app.route("/set_webhook")
async def set_webhook_route():
    if not WEBHOOK_URL:
        return "Ошибка: WEBHOOK_URL не задан в переменных окружения!", 500
    
    webhook_full_url = f"{WEBHOOK_URL}/webhook"
    await ptb_app.bot.set_webhook(url=webhook_full_url, allowed_updates=Update.ALL_TYPES)
    
    # Проверяем, что вебхук действительно установился
    webhook_info = await ptb_app.bot.get_webhook_info()
    
    return f"Вебхук установлен на: {webhook_info.url}", 200

# --- УДАЛЯЕМ СТАРЫЙ БЛОК if __name__ == "__main__" ---
# Он нам больше не нужен, gunicorn будет запускать 'app' напрямую.
