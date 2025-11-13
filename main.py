# main.py

import logging
import asyncio
import sys
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

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- НАСТРОЙКА ВЕБ-СЕРВЕРА ---
# Render предоставит порт через переменную окружения PORT
PORT = int(os.environ.get('PORT', 8443))
# URL, на который Telegram будет отправлять обновления. Укажите его в переменных окружения на Render.
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

# Создаем Flask-приложение. 'app' - это имя, которое gunicorn будет искать.
app = Flask(__name__)

# --- ОСНОВНАЯ ЛОГИКА БОТА (остается почти без изменений) ---
def setup_application() -> Application:
    """Создает и настраивает экземпляр Application."""
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

# Создаем экземпляр приложения один раз при запуске
ptb_app = setup_application()

# --- КОНЕЧНЫЕ ТОЧКИ (ЭНДПОИНТЫ) ДЛЯ ВЕБ-СЕРВЕРА ---

@app.route("/")
def index():
    """Эндпоинт для проверки здоровья сервиса. Render будет его проверять."""
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
async def webhook():
    """Этот эндпоинт принимает обновления от Telegram."""
    update_data = request.get_json()
    update = Update.de_json(update_data, ptb_app.bot)
    await ptb_app.process_update(update)
    return "OK", 200

# --- ЗАПУСК И НАСТРОЙКА ВЕБХУКА ---
# Эта часть выполняется только при запуске скрипта напрямую, а не через gunicorn.
# Она нужна, чтобы один раз "зарегистрировать" наш вебхук в Telegram.
async def setup_webhook():
    """Устанавливает вебхук."""
    if not WEBHOOK_URL:
        logger.error("WEBHOOK_URL не задан!")
        return
    
    # URL должен заканчиваться на /webhook, как в @app.route
    webhook_full_url = f"{WEBHOOK_URL}/webhook"
    
    await ptb_app.bot.set_webhook(url=webhook_full_url, allowed_updates=Update.ALL_TYPES)
    logger.info(f"Вебхук успешно установлен на: {webhook_full_url}")

if __name__ == "__main__":
    # Эта команда нужна, чтобы один раз установить вебхук.
    # После первого успешного деплоя ее можно закомментировать или удалить.
    asyncio.run(setup_webhook())
    
    # При локальном запуске для теста можно использовать:
    # app.run(host="0.0.0.0", port=PORT)
    # Но на Render будет использоваться gunicorn.
