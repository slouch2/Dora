# utils/time_utils.py

from datetime import datetime, timezone, timedelta

def get_current_time():
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst)
    return now.strftime("%Y-%m-%d %H:%M:%S")
