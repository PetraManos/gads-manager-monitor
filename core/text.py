from __future__ import annotations
import re

def norm(s: object) -> str:
    """Lowercase, convert NBSP to space, strip."""
    return str(s or "").lower().replace("\u00A0", " ").strip()

def collapse_one_line(s: str) -> str:
    """Collapse all whitespace to single spaces and trim."""
    return re.sub(r"\s+", " ", s or "").strip()

def has_word(s: str, word: str) -> bool:
    """Whole-word match (case-insensitive)."""
    s_l = (s or "").lower()
    w = re.escape((word or "").lower())
    return re.search(rf"(^|\W){w}(?=$|\W)", s_l) is not None

# ---- added to satisfy core/__init__.py imports ----
def norm_collapse(s: object) -> str:
    """Normalize then collapse to a single line."""
    return collapse_one_line(norm(s))

def make_key(*parts: object) -> str:
    """Stable pipe-delimited key based on normalized, collapsed parts."""
    return "|".join(norm_collapse(p) for p in parts)
# ---------------------------------------------------

__all__ = [
    "norm",
    "collapse_one_line",
    "has_word",
    "norm_collapse",
    "make_key",
]
