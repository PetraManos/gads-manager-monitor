from __future__ import annotations
from decimal import Decimal

def as_number(x: object) -> float | None:
    """Best-effort numeric parser for strings with commas/percent signs."""
    if x is None:
        return None
    s = str(x).strip()
    if s == "":
        return None
    # Handle negatives like (1,234.56)
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg = True
        s = s[1:-1].strip()
    # Strip currency symbols and spaces
    s = s.replace("$", "").replace("€", "").replace("£", "").replace("AUD", "").replace("USD", "")
    s = s.replace(",", "").strip()
    # Strip trailing percent for generic parsing
    if s.endswith("%"):
        s = s[:-1].strip()
    try:
        v = float(s)
        return -v if neg else v
    except Exception:
        return None

# Back-compat alias expected by core/__init__.py
to_num = as_number

def parse_money_cell(x: object) -> float | None:
    """Parse currency-like strings to a float amount (None if not parseable)."""
    return as_number(x)

def parse_percent_cell(x: object) -> float | None:
    """
    Parse percent-like strings to numeric percent value (e.g., '12.5%' -> 12.5).
    Returns None if not parseable.
    """
    if x is None:
        return None
    s = str(x).strip()
    if s == "":
        return None
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg = True
        s = s[1:-1].strip()
    # Keep percent semantics: if '%' present, remove it; otherwise assume already a percent number
    has_pct = s.endswith("%")
    if has_pct:
        s = s[:-1].strip()
    s = s.replace("$", "").replace("€", "").replace("£", "").replace("AUD", "").replace("USD", "")
    s = s.replace(",", "").strip()
    try:
        v = float(s)
        v = -v if neg else v
        return v
    except Exception:
        return None

def to_currency(x: float | Decimal | int, symbol: str = "$", places: int = 2) -> str:
    """Format a number as currency with thousands separators."""
    try:
        return f"{symbol}{float(x):,.{places}f}"
    except Exception:
        return f"{symbol}0.00"

__all__ = [
    "as_number",
    "to_num",
    "parse_money_cell",
    "parse_percent_cell",
    "to_currency",
]
