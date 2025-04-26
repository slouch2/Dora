from core.trade_executor import market_buy, market_sell

# 매매 함수 예시

def execute_trade(signal, ticker, current_price, available_krw, quantity):
    max_trade_per_coin = 1000000  # 종목당 최대 100만원
    min_order_amount = 5000        # 최소 주문 금액 5천원

    if signal == "buy":
        krw_amount = min(available_krw, max_trade_per_coin)
        if krw_amount >= min_order_amount:
            market_buy(ticker, krw_amount)
        else:
            print(f"[매수 실패] 주문 가능 금액 부족: {krw_amount} KRW")
    
    elif signal == "sell":
        if quantity > 0:
            market_sell(ticker, quantity)
        else:
            print(f"[매도 실패] 보유 수량 없음")
    
    elif signal == "hold":
        print(f"[대기] {ticker} 아무것도 안함")
