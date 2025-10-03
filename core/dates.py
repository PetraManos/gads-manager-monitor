# core/dates.py
from __future__ import annotations
from datetime import datetime, date, timedelta, timezone

# Prefer system tzdata; fall back to fixed ACST/ACDT-like offset if unavailable.
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:
    ZoneInfo = None  # type: ignore

# Default timezone to match the script's Adelaide setting
_DEFAULT_TZ_NAME = "Australia/Adelaide"
_FALLBACK_TZ = timezone(timedelta(hours=9, minutes=30))  # ACST fallback (no DST)


def _tz():
    """Resolve Australia/Adelaide if tzdata is present; otherwise use a fixed offset."""
    if ZoneInfo is not None:
        try:
            return ZoneInfo(_DEFAULT_TZ_NAME)
        except Exception:
            pass
    return _FALLBACK_TZ


def _at_midnight_local(dt: datetime) -> datetime:
    """Truncate a datetime to midnight in local TZ."""
    local = dt.astimezone(_tz())
    return local.replace(hour=0, minute=0, second=0, microsecond=0)


def _yyyymmdd(d: datetime | date) -> str:
    if isinstance(d, datetime):
        d = d.date()
    return f"{d.year:04d}{d.month:02d}{d.day:02d}"


def normalize_date_only(d: datetime | date) -> datetime:
    """
    GS parity of normalizeDate_(d): return the same calendar date at 00:00:00 in local TZ.
    """
    if isinstance(d, datetime):
        return _at_midnight_local(d)
    # date -> interpret as local TZ midnight
    return datetime(d.year, d.month, d.day, tzinfo=_tz())


def ymd(d: datetime | date | None = None) -> str:
    """
    GS parity of ymd(d): Utilities.formatDate(d, tz, 'yyyyMMdd').
    If d is None, use 'today' in local TZ.
    """
    if d is None:
        d = _at_midnight_local(datetime.now(tz=_tz()))
    elif isinstance(d, datetime):
        d = _at_midnight_local(d)
    else:  # date
        d = datetime(d.year, d.month, d.day, tzinfo=_tz())
    return _yyyymmdd(d)


def range_last_n_days(n: int) -> str:
    """
    GS parity of rangeLastNDays(n): inclusive 'yyyyMMdd,yyyyMMdd' in local TZ.
    start = today - (n-1); end = today.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    end = _at_midnight_local(datetime.now(tz=_tz()))
    start = end - timedelta(days=n - 1)
    return f"{_yyyymmdd(start)},{_yyyymmdd(end)}"


__all__ = ["ymd", "range_last_n_days", "normalize_date_only"]
