# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API
OPENAI_API_KEY = "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"

# Upbit API
UPBIT_ACCESS_KEY = "gMHb9heXbI9Jvz2VoeH7avAhah1Qb9aNhcqDxD6W"
UPBIT_SECRET_KEY = "N2f1Nyt9smProScfKJpplu4z9lhgHeqfxQvVxVQo"

# Telegram
TELEGRAM_TOKEN = "7559159179:AAHrwuPffBgwFV23HWOY1P8Zl31_6Ol4OJo"
TELEGRAM_CHAT_ID = "7367082920"

# 매매 설정
MAX_TRADE_PER_COIN = 1000000  # 한 종목당 최대 100만원
MIN_ORDER_AMOUNT = 5000  # 업비트 최소 주문금액
TRADING_FEE_RATE = 0.005  # 업비트 수수료 0.05%

# Streamlit
STREAMLIT_PORT = 8501

# GitHub Token
GITHUB_TOKEN = "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"
