# core/string_utils.py
from __future__ import annotations
import re

_NBSP = "\u00A0"
_WS = re.compile(r"\s+")

def norm(s: object) -> str:
    """
    Exact replica of core_shared.gs norm():
    - None → ""
    - Cast to str
    - Replace NBSP with space
    - Collapse all whitespace to single space
    - Trim
    - Lowercase
    """
    text = "" if s is None else str(s)
    text = text.replace(_NBSP, " ")
    text = _WS.sub(" ", text).strip().lower()
    return text

def collapse_one_line(s: str) -> str:
    """Collapse all whitespace to single spaces and trim (case-preserving)."""
    return re.sub(r"\s+", " ", s or "").strip()

def has_word(s: str, word: str) -> bool:
    """
    Whole-word match (case-insensitive), with custom boundaries where
    hyphen/underscore are treated as part of a word (so 'red-blue' does NOT match 'blue').
    """
    text = (s or "").lower()
    w = re.escape((word or "").lower())
    # Word chars include letters/digits/underscore/hyphen. Boundaries are the inverse of that set.
    pattern = rf"(?<![A-Za-z0-9_-]){w}(?![A-Za-z0-9_-])"
    return re.search(pattern, text) is not None

def has_match_type_token(name: object) -> bool:
    """
    Detect 'exact match' / 'phrase match' / 'broad match' with optional spaces/hyphens/underscores
    between the words, case-insensitive. Examples: 'Exact Match', 'phrase-match', 'BROAD_match'.
    """
    s = ("" if name is None else str(name)).lower()
    pattern = r"(?<![A-Za-z0-9_-])(?:exact|phrase|broad)[\s\-_]*match(?![A-Za-z0-9_-])"
    return re.search(pattern, s) is not None

# ---- helpers used elsewhere ----
def norm_collapse(s: object) -> str:
    """Normalize then collapse to a single line."""
    return collapse_one_line(norm(s))

def make_key(*parts: object) -> str:
    """Stable pipe-delimited key based on normalized, collapsed parts."""
    return "|".join(norm_collapse(p) for p in parts)
# -------------------------------

__all__ = [
    "norm",
    "collapse_one_line",
    "has_word",
    "has_match_type_token",
    "norm_collapse",
    "make_key",
]
