# utils/telegram_bot.py

import telegram
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = telegram.Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
