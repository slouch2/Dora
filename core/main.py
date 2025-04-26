import time
import openai
import pyupbit
from config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY, OPENAI_API_KEY
from core.trade_executor import market_buy, market_sell
from core.balance_checker import get_balance_info

openai.api_key = OPENAI_API_KEY
upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

MAX_TRADE_PER_COIN = 1000000  # 종목당 최대 100만원
MIN_ORDER_AMOUNT = 5000       # 업비트 최소 주문 금액

def get_candidate_coins():
    tickers = pyupbit.get_tickers(fiat="KRW")
    filtered = []
    for ticker in tickers:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="day", count=1200)  # 약 5년 데이터
            if df is not None and len(df) >= 1200:
                filtered.append(ticker)
        except Exception:
            continue
    volumes = {}
    for ticker in filtered:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="minute5", count=2)
            if df is not None:
                volumes[ticker] = df['volume'][-1]
        except Exception:
            continue
    sorted_coins = sorted(volumes.items(), key=lambda x: x[1], reverse=True)
    top5 = [coin[0] for coin in sorted_coins[:5]]
    return top5

def get_trade_signal(ticker):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 트레이딩 전문가야. 매수할지 매도할지 대기할지 판단해."},
                {"role": "user", "content": f"{ticker} 5분봉 차트와 거래량 데이터를 기반으로 'buy', 'sell', 'hold' 중 하나를 추천해줘."}
            ]
        )
        decision = response['choices'][0]['message']['content'].lower()
        if "buy" in decision:
            return "buy"
        elif "sell" in decision:
            return "sell"
        else:
            return "hold"
    except Exception as e:
        print(f"오류 발생 (OpenAI 호출 실패): {e}")
        return "hold"

def execute_trade():
    cash, _, _ = get_balance_info()
    owned = pyupbit.get_balances()

    # 매도 체크
    for asset in owned:
        if asset['currency'] == 'KRW' or float(asset['balance']) == 0:
            continue
        ticker = f"KRW-{asset['currency']}"
        signal = get_trade_signal(ticker)
        if signal == "sell":
            balance = float(asset['balance'])
            market_sell(ticker, balance)

    # 매수 체크
    if cash >= MIN_ORDER_AMOUNT:
        candidate_coins = get_candidate_coins()
        split_cash = min(MAX_TRADE_PER_COIN, cash)  # 종목당 최대 100만원 제한
        per_coin_cash = split_cash

        for ticker in candidate_coins:
            if cash < MIN_ORDER_AMOUNT:
                break
            signal = get_trade_signal(ticker)
            if signal == "buy":
                price = pyupbit.get_current_price(ticker)
                if price is None:
                    continue
                volume = per_coin_cash / price
                market_buy(ticker, volume)
                cash -= per_coin_cash
                time.sleep(1)

if __name__ == "__main__":
    while True:
        try:
            execute_trade()
            print("✅ 매매 루프 1회 완료")
        except Exception as e:
            print(f"오류 발생: {e}")
        time.sleep(300)  # 5분 대기
