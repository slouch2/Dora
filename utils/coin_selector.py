# utils/coin_selector.py

import pyupbit
from datetime import datetime, timedelta

def get_top_coins():
    tickers = pyupbit.get_tickers(fiat="KRW")
    volumes = {}

    for ticker in tickers:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
            if df is not None:
                total_volume = df['value'][-1]
                volumes[ticker] = total_volume
        except Exception as e:
            continue

    sorted_volumes = sorted(volumes.items(), key=lambda x: x[1], reverse=True)

    # 상장된 지 5년 이상된 코인만 필터링
    five_years_ago = datetime.now() - timedelta(days=5*365)

    eligible_tickers = []
    for ticker, _ in sorted_volumes:
        try:
            df = pyupbit.get_ohlcv(ticker, interval="day", count=1000)
            if df is not None:
                oldest_date = df.index.min()
                if oldest_date <= five_years_ago:
                    eligible_tickers.append(ticker.replace("KRW-", ""))
        except:
            continue

        if len(eligible_tickers) >= 5:
            break

    return eligible_tickers
