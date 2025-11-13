# main.py

import logging
import asyncio
import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from contextlib import asynccontextmanager

import config
import database
from handlers import start_handler, topic_handler, difficulty_handler, feedback_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

def setup_application() -> Application:
    if not config.TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN не найден!")

    application = (
        Application.builder()
        .token(config.TELEGRAM_TOKEN)
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Выполняется один раз при старте и один раз при остановке сервера."""
    logger.info("Запуск приложения...")
    await ptb_app.initialize()
    await database.connect_db()
    
    if WEBHOOK_URL:
        await ptb_app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook", allowed_updates=Update.ALL_TYPES)
        logger.info(f"Вебхук успешно установлен на: {WEBHOOK_URL}/webhook")
    else:
        logger.warning("WEBHOOK_URL не задан, вебхук не будет установлен!")
    
    yield  # Приложение работает здесь
    
    logger.info("Остановка приложения...")
    await database.close_db_pool()
    await ptb_app.shutdown()

# Создаем FastAPI приложение с жизненным циклом
app = FastAPI(lifespan=lifespan)

@app.get("/")
def index():
    return {"status": "Bot is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    update_data = await request.json()
    update = Update.de_json(update_data, ptb_app.bot)
    await ptb_app.process_update(update)
    return {"status": "ok"}
