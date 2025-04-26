import pyupbit
from config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY

upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

def market_buy(ticker, volume):
    try:
        result = upbit.buy_market_order(ticker, volume)
        print(f"[매수 성공] {ticker} {volume}개 시장가 매수 완료")
        return result
    except Exception as e:
        print(f"[매수 실패] {ticker}: {e}")
        return None

def market_sell(ticker, volume):
    try:
        result = upbit.sell_market_order(ticker, volume)
        print(f"[매도 성공] {ticker} {volume}개 시장가 매도 완료")
        return result
    except Exception as e:
        print(f"[매도 실패] {ticker}: {e}")
        return None
