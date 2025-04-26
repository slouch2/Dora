# core/trade_executor.py

import pyupbit
from config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY, TRADING_FEE_RATE, MIN_ORDER_AMOUNT, MAX_TRADE_PER_COIN

upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

async def execute_trade(coin, decision):
    ticker = f"KRW-{coin}"

    if decision == "buy":
        price = pyupbit.get_current_price(ticker)
        volume = (MAX_TRADE_PER_COIN * (1 - TRADING_FEE_RATE)) / price
        amount = price * volume

        if amount < MIN_ORDER_AMOUNT:
            return {"status": "fail", "reason": "Amount below minimum"}

        response = upbit.buy_market_order(ticker, volume)
        return response

    elif decision == "sell":
        balance = upbit.get_balance(ticker)

        if balance > 0:
            response = upbit.sell_market_order(ticker, balance)
            return response
        else:
            return {"status": "fail", "reason": "No balance"}

    else:
        return {"status": "hold"}

