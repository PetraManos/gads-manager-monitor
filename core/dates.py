from __future__ import annotations
from datetime import datetime, date, timedelta, timezone

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # Python 3.9+
except Exception:  # environments without tzdata
    ZoneInfo = None  # type: ignore
    class ZoneInfoNotFoundError(Exception):
        ...

# Adelaide fallback if tzdata missing (no DST in fallback)
_DEF_FIXED_OFFSET = timezone(timedelta(hours=9, minutes=30))

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
    """Override the module timezone (useful for tests)."""
    global _TZ
    _TZ = tz

def now_tz() -> datetime:
    return datetime.now(tz=_TZ)

def now() -> datetime:
    """Alias expected by core/__init__.py; timezone-aware Adelaide-now (or fallback)."""
    return now_tz()

def ymd(dt: datetime | date | None = None) -> str:
    """Return YYYY-MM-DD from a datetime/date (defaults to now())."""
    if dt is None:
        dt = now_tz()
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.strftime("%Y-%m-%d")

def normalize_date(value: datetime | date | str | None) -> str:
    """
    Best-effort normalizer to YYYY-MM-DD.
    Accepts datetime/date or common string formats:
      - YYYY-MM-DD
      - DD/MM/YYYY
      - MM/DD/YYYY
      - YYYY/MM/DD
      - YYYY.MM.DD
    Falls back to today's date if value is None/empty.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return ymd()

    if isinstance(value, (datetime, date)):
        return ymd(value)

    s = value.strip()
    # Fast path: ISO-like YYYY-MM-DD
    try:
        return datetime.fromisoformat(s).date().strftime("%Y-%m-%d")
    except Exception:
        pass

    # Try a handful of explicit formats
    fmts = ["%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%Y.%m.%d"]
    for f in fmts:
        try:
            return datetime.strptime(s, f).date().strftime("%Y-%m-%d")
        except Exception:
            continue

    # If all parsing fails, return as-is if it looks like YYYY-MM-DD, else today.
    # (Keeps behavior predictable without adding heavy deps.)
    try:
        # len check to avoid ValueError from slicing weird strings
        if len(s) >= 10:
            datetime.strptime(s[:10], "%Y-%m-%d")
            return s[:10]
    except Exception:
        pass

    return ymd()

def range_last_n_days(n: int) -> tuple[str, str]:
    end = now_tz().date()
    start = end - timedelta(days=n)
    return (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

__all__ = ["set_tz", "now_tz", "now", "ymd", "normalize_date", "range_last_n_days"]
