from datetime import datetime, timedelta, timezone
try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except Exception:  # Pyodide / missing tzdata
    ZoneInfo = None  # type: ignore
    class ZoneInfoNotFoundError(Exception): ...
_DEF_FIXED_OFFSET = timezone(timedelta(hours=9, minutes=30))  # Adelaide fallback

def _resolve_adelaide_tz():
    try:
        if ZoneInfo is not None:
            return ZoneInfo("Australia/Adelaide")
    except ZoneInfoNotFoundError:
        pass
    except Exception:
        pass
    return _DEF_FIXED_OFFSET

_TZ = _resolve_adelaide_tz()

def set_tz(tz: timezone) -> None:
    global _TZ
    _TZ = tz

def now_tz() -> datetime:
    return datetime.now(tz=_TZ)

def ymd(dt: datetime | None = None) -> str:
    dt = dt or now_tz()
    return dt.strftime("%Y-%m-%d")

def range_last_n_days(n: int) -> tuple[str, str]:
    end = now_tz().date()
    start = end - timedelta(days=n)
    return (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
