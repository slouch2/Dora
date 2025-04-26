# core/decision_maker.py

import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def make_decision(coin, strategy_data):
    prompt = f"""
You're an expert in coin investing. Tell us whether to buy, sell, or hold based on the chart data and indicators provided.

Coin: {coin}
Data: {strategy_data}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-05-13",  # 가장 저렴하고 빠른 4o-mini
        messages=[
            {"role": "system", "content": "You are a professional cryptocurrency investor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    reply = response['choices'][0]['message']['content'].lower()

    if "buy" in reply:
        return "buy", reply
    elif "sell" in reply:
        return "sell", reply
    else:
        return "hold", reply
