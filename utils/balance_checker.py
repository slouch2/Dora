# utils/balance_checker.py

import pyupbit
from config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY

upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

def get_balance_info():
    balances = upbit.get_balances()
    cash = 0
    coin_value = 0

    for balance in balances:
        currency = balance['currency']
        if currency == "KRW":
            cash = float(balance['balance'])
        else:
            quantity = float(balance['balance'])
            if quantity > 0:
                ticker = f"KRW-{currency}"
                price = 0
                try:
                    price = pyupbit.get_current_price(ticker)
                    if price is None:
                        price = 0
                except Exception as e:
                    print(f"[경고] {ticker} 가격 조회 실패, 오류 무시하고 진행합니다.")

                coin_value += quantity * price  # 가격이 0이면 평가 금액 0으로 들어감

    total_asset = cash + coin_value
    return cash, coin_value, total_asset
