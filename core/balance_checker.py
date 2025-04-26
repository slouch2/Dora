import pyupbit
from config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY

upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

def get_balance_info():
    try:
        balances = upbit.get_balances()
        cash = 0
        coin_value = 0
        total_asset = 0

        for b in balances:
            if b['currency'] == "KRW":
                cash = float(b['balance'])
            else:
                coin = b['currency']
                quantity = float(b['balance'])
                if quantity > 0:
                    price = pyupbit.get_current_price(f"KRW-{coin}")
                    if price:
                        coin_value += quantity * price
        total_asset = cash + coin_value
        return cash, coin_value, total_asset
    except Exception as e:
        print(f"[잔고 조회 실패]: {e}")
        return 0, 0, 0
