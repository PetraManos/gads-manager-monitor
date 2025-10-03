from datetime import datetime, date, timedelta, timezone
from core.dates import ymd, range_last_n_days, normalize_date_only

def _is_yyyymmdd(s: str) -> bool:
    return isinstance(s, str) and len(s) == 8 and s.isdigit()

def test_ymd_default_today_format():
    out = ymd()
    assert _is_yyyymmdd(out)

def test_ymd_with_date_literal():
    assert ymd(date(2025, 10, 3)) == "20251003"

def test_ymd_with_datetime_truncates_to_local_midnight():
    # Pick a UTC time that may roll over after converting to Adelaide;
    # expected should be computed in local TZ, not assumed.
    dt_utc = datetime(2025, 10, 3, 15, 47, tzinfo=timezone.utc)
    expected = ymd(normalize_date_only(dt_utc))
    out = ymd(dt_utc)
    assert out == expected

def test_normalize_date_only_truncates_and_sets_tzinfo():
    dt = datetime(2025, 10, 3, 22, 15, tzinfo=timezone.utc)
    norm = normalize_date_only(dt)
    assert norm.hour == 0 and norm.minute == 0 and norm.second == 0 and norm.microsecond == 0
    assert norm.tzinfo is not None  # localized

def test_range_last_n_days_inclusive_format_and_end_matches_today():
    n = 7
    s = range_last_n_days(n)
    assert "," in s
    start, end = s.split(",", 1)
    assert _is_yyyymmdd(start) and _is_yyyymmdd(end)
    assert end == ymd()

def test_range_last_n_days_inclusive_window_math():
    n = 7
    today_local_midnight = normalize_date_only(datetime.now(timezone.utc))
    expected_start = ymd(today_local_midnight - timedelta(days=n - 1))
    start, end = range_last_n_days(n).split(",", 1)
    assert start == expected_start
    assert start <= end  # lexical compare works for yyyymmdd

def test_range_last_n_days_rejects_n_lt_1():
    import pytest
    with pytest.raises(ValueError):
        range_last_n_days(0)
