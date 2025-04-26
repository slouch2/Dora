# utils/data_collector.py

import pyupbit

def collect_data(coin):
    ticker = f"KRW-{coin}"

    # 1. 현재 가격
    current_price = pyupbit.get_current_price(ticker)

    # 2. 캔들 데이터
    df = pyupbit.get_ohlcv(ticker, interval="day", count=200)

    # 3. RSI 계산
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    latest_rsi = rsi.iloc[-1]

    # 4. MACD 계산
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    latest_macd = macd_line.iloc[-1]
    latest_signal = signal_line.iloc[-1]

    # 5. Stochastic 계산
    low_min = df['low'].rolling(window=14).min()
    high_max = df['high'].rolling(window=14).max()
    stoch_k = ((df['close'] - low_min) / (high_max - low_min)) * 100
    stoch_d = stoch_k.rolling(window=3).mean()
    latest_stoch_k = stoch_k.iloc[-1]
    latest_stoch_d = stoch_d.iloc[-1]

    # 6. 거래량 데이터
    current_volume = df['volume'].iloc[-1]
    volume_ma30 = df['volume'].rolling(window=30).mean().iloc[-1]

    # 7. 이동평균선
    ma200 = df['close'].rolling(window=200).mean().iloc[-1]
    ma200_slope = ma200 - df['close'].rolling(window=200).mean().iloc[-2]

    ema20 = df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
    ema50 = df['close'].ewm(span=50, adjust=False).mean().iloc[-1]

    # 8. 볼린저밴드
    bb_center = df['close'].rolling(20).mean().iloc[-1]
    bb_std = df['close'].rolling(20).std().iloc[-1]
    bb_upper = bb_center + 2 * bb_std
    bb_lower = bb_center - 2 * bb_std

    if current_price >= bb_upper:
        bb_position = "Upper Band"
    elif current_price <= bb_lower:
        bb_position = "Lower Band"
    else:
        bb_position = "Middle Band"

    # 9. 호가 데이터
    orderbook = pyupbit.get_orderbook(ticker)
    bid_ask_spread = None
    if orderbook:
        bids = orderbook[0]['orderbook_units'][0]['bid_price']
        asks = orderbook[0]['orderbook_units'][0]['ask_price']
        bid_ask_spread = (asks - bids) / bids * 100

    # 데이터 패키징
    data = {
        "current_price": current_price,
        "RSI": latest_rsi,
        "MACD": latest_macd,
        "MACD_signal": latest_signal,
        "Stochastic_K": latest_stoch_k,
        "Stochastic_D": latest_stoch_d,
        "current_volume": current_volume,
        "volume_MA30": volume_ma30,
        "200MA_value": ma200,
        "200MA_slope": ma200_slope,
        "20EMA": ema20,
        "50EMA": ema50,
        "Bollinger_position": bb_position,
        "bid_ask_spread": bid_ask_spread
    }

    return data
