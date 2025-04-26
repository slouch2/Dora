# core/monitor_streamlit.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.balance_checker import get_balance_info
import streamlit as st
import json
import os
import time
from datetime import datetime, timezone, timedelta

LOG_PATH = "trades.json"

def get_kst_now():
    kst = timezone(timedelta(hours=9))
    return datetime.now(kst)

def load_trades():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            trades = json.load(f)
    else:
        trades = []
    return trades

def calculate_stats(trades):
    wins = sum(1 for t in trades if t.get("result", {}).get("profit", 0) > 0)
    total = len(trades)
    win_rate = (wins / total) * 100 if total > 0 else 0.0
    return win_rate

def calculate_buy_amount(trades):
    total_buy = sum(t.get("result", {}).get("price", 0) * t.get("result", {}).get("volume", 0) for t in trades if t.get("decision") == "buy")
    return total_buy

def run_dashboard():
    st.set_page_config(page_title="도라 실시간 매매 대시보드", layout="wide")
    st.title("🚀 도라 실시간 매매 대시보드")

    start_time = get_kst_now()
    start_capital = 1000000  # 시작 원금 100만원 고정

    placeholder = st.empty()

    while True:
        now = get_kst_now()
        cash, coin_value, total_asset = get_balance_info()
        trades = load_trades()

        invest_time = now - start_time
        win_rate = calculate_stats(trades)
        profit_rate = ((total_asset - start_capital) / start_capital) * 100
        profit_rate = round(profit_rate, 2)  # 소수점 둘째자리까지 반올림
        total_buy = calculate_buy_amount(trades)
        total_eval = coin_value

        with placeholder.container():
            st.subheader("📈 자산 현황")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("보유 KRW", f"{cash:,.0f} KRW")
            with col2:
                st.metric("총 보유자산", f"{total_asset:,.0f} KRW")
            with col3:
                st.metric("총 매수금액", f"{total_buy:,.0f} KRW")

            col4, col5, col6 = st.columns(3)
            with col4:
                st.metric("총 평가금액", f"{total_eval:,.0f} KRW")
                st.metric("시작금", f"{start_capital:,.0f} KRW")
            with col5:
                st.metric("주문 가능 금액", f"{cash:,.0f} KRW")
            with col6:
                st.metric("투자 기간", str(invest_time).split('.')[0])  # 초 단위까지

            st.metric("승률", f"{win_rate:.2f} %")
            st.metric("수익률", f"{profit_rate:.2f} %")

            st.subheader("📄 최근 매매 기록")
            if trades:
                records = []
                for t in trades:
                    record = {
                        "timestamp": t.get("time"),
                        "trade_type": t.get("decision"),
                        "ticker": t.get("coin"),
                        "price": t.get("result", {}).get("price", "N/A"),
                        "volume": t.get("result", {}).get("volume", "N/A"),
                        "reason": t.get("reason", "N/A"),
                        "profit_rate": t.get("result", {}).get("profit_rate", "N/A"),
                    }
                    records.append(record)

                st.dataframe(records, use_container_width=True)
            else:
                st.warning("아직 매매 기록이 없습니다.")

        time.sleep(5)

if __name__ == "__main__":
    run_dashboard()
