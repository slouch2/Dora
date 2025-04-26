# main.py

import asyncio
from core.decision_maker import make_decision
from core.trade_executor import execute_trade
from core.trade_logger import log_trade
from utils.telegram_bot import send_telegram_message
from utils.coin_selector import get_top_coins
from utils.time_utils import get_current_time
import streamlit as st

async def main():
    # 1. 거래할 코인 선정
    target_coins = get_top_coins()

    # 2. 각 코인에 대해 매매 판단 및 실행
    for coin in target_coins:
        strategy_data = {}  # 전략 데이터는 나중에 입력
        decision, reason = await make_decision(coin, strategy_data)
        if decision in ["buy", "sell", "hold"]:
            result = await execute_trade(coin, decision)
            log_trade(coin, decision, reason, result)
            await send_telegram_message(f"{coin} {decision.upper()} - Reason: {reason}")

if __name__ == "__main__":
    asyncio.run(main())
