# core/trade_logger.py

import json
import os
from utils.time_utils import get_current_time

LOG_PATH = "trades.json"

def log_trade(coin, decision, reason, result):
    trade = {
        "time": get_current_time(),
        "coin": coin,
        "decision": decision,
        "reason": reason,
        "result": result
    }

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            trades = json.load(f)
    else:
        trades = []

    trades.append(trade)

    with open(LOG_PATH, "w") as f:
        json.dump(trades, f, indent=4)
