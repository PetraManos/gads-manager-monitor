from __future__ import annotations
from typing import Optional
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def ymd(dt: Optional[datetime]=None, tz: str="UTC") -> str:
    tzinfo = ZoneInfo(tz)
    dt = (dt or datetime.now(tzinfo)).astimezone(tzinfo)
    return dt.strftime("%Y%m%d")

def range_last_n_days(n: int, tz: str="UTC") -> str:
    tzinfo = ZoneInfo(tz)
    end = datetime.now(tzinfo)
    start = end - timedelta(days=max(0, n-1))
    return f"{start.strftime('%Y%m%d')},{end.strftime('%Y%m%d')}"

def normalize_date(dt: datetime, tz: str="UTC") -> datetime:
    tzinfo = ZoneInfo(tz)
    dt = dt.astimezone(tzinfo)
    return datetime(dt.year, dt.month, dt.day, tzinfo=tzinfo)

def now(tz: str="UTC") -> datetime:
    return datetime.now(ZoneInfo(tz))
