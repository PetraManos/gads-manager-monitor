from __future__ import annotations
from typing import Any
import re

def to_num(x: Any) -> float:
    try:
        s = re.sub(",", "", str(x or "0"))
        return float(s)
    except Exception:
        return 0.0

def as_number(v: Any) -> float:
    """Parse number or percent-like strings. Returns ratio (e.g. '5%' -> 0.05)."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v or "").strip()
    if not s: return float("nan")
    m = re.search(r"-?\d+(\.\d+)?", s)
    if not m: return float("nan")
    n = float(m.group(0))
    if "%" in s: n /= 100.0
    return n

def parse_money_cell(v: Any) -> float:
    if isinstance(v, (int, float)):
        return float(v) or 0.0
    s = str(v or "").replace("$","").replace(",","").strip()
    try:
        return float(s)
    except Exception:
        s2 = re.sub(r"[^0-9.\-]", "", s) or "0"
        return float(s2)

def parse_percent_cell(v: Any) -> float:
    """Return percent value (Apps Script behaviour: 0.5 -> 50)."""
    if isinstance(v, (int, float)):
        return v*100 if 0 < v < 1 else float(v)
    s = str(v or "").strip()
    if not s: return float("nan")
    if s.endswith("%"): s = s[:-1]
    try:
        n = float(s)
        return n*100 if 0 < n < 1 else n
    except Exception:
        return float("nan")

def to_currency(val: Any) -> float:
    raw = str("" if val is None else val).strip()
    if not raw: return 0.0
    try:
        n = float(raw)
    except Exception:
        n = float(re.sub(r"[^0-9.\-]", "", raw) or "0")
    return n/1e6 if abs(n) >= 100000 else n
