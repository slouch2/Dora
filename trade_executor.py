# core/trade_executor.py

import pyupbit
from config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY, MIN_ORDER_AMOUNT

upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

# 시장가 매수
def market_buy(ticker, krw_amount):
    if krw_amount < MIN_ORDER_AMOUNT:
        print(f"[매수 실패] 최소 주문 금액({MIN_ORDER_AMOUNT}원) 미만입니다.")
        return None
    try:
        response = upbit.buy_market_order(ticker, krw_amount)
        print(f"[매수 완료] {ticker} {krw_amount} KRW 시장가 매수")
        return response
    except Exception as e:
        print(f"[매수 오류] {e}")
        return None

# 시장가 매도
def market_sell(ticker, quantity):
    if quantity <= 0:
        print(f"[매도 실패] 보유 수량이 없습니다.")
        return None
    try:
        response = upbit.sell_market_order(ticker, quantity)
        print(f"[매도 완료] {ticker} {quantity}개 시장가 매도")
        return response
    except Exception as e:
        print(f"[매도 오류] {e}")
        return None
