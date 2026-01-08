import os
import time
from collections import defaultdict, deque

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from model import LLMService

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
if not TOKEN:
    raise RuntimeError("Не задан TELEGRAM_BOT_TOKEN в .env (смотри .env.example)")

llm = LLMService()

# Простая защита: ограничение частоты сообщений
REQ_PER_MIN = 6
user_hits = defaultdict(lambda: deque())  # user_id -> timestamps


def is_rate_limited(user_id: int) -> bool:
    now = time.time()
    q = user_hits[user_id]
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= REQ_PER_MIN:
        return True
    q.append(now)
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Telegram-бот с интеграцией LLM через Ollama.\n"
        "Напиши любой вопрос — я отвечу.\n\n"
        "Команды: /start, /help"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Как запустить:\n"
        "1) Установи Ollama и скачай модель (например gemma3:4b)\n"
        "2) Создай .env по образцу .env.example\n"
        "3) Установи зависимости: python -m pip install -r requirements.txt\n"
        "4) Запусти: python bot.py"
    )


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_rate_limited(user_id):
        await update.message.reply_text("Слишком часто 🙂 Подожди минуту и попробуй снова.")
        return

    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("Напиши текст запроса 🙂")
        return

    await update.message.chat.send_action("typing")
    answer = llm.generate(text)
    await update.message.reply_text(answer)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    print("Bot started. Press Ctrl+C to stop.")
    import asyncio
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app.run_polling()


if __name__ == "__main__":
    main()
