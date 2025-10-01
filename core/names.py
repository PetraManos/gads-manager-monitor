from __future__ import annotations
from enum import Enum
from core.text import norm

class MatchType(str, Enum):
    BROAD = "BROAD"
    PHRASE = "PHRASE"
    EXACT = "EXACT"

# canonical tokens used in names
_TOKEN_TO_TYPE = {
    "[broad]": MatchType.BROAD,
    "[phrase]": MatchType.PHRASE,
    "[exact]": MatchType.EXACT,
}
_TYPE_TO_TOKEN = {v: k for k, v in _TOKEN_TO_TYPE.items()}

_BRAND_TOKENS = {"brand", "branded"}

def has_match_type_token(name: str) -> bool:
    n = norm(name)
    return any(tok in n for tok in _TOKEN_TO_TYPE.keys())

def declared_type(name: str) -> MatchType | None:
    """
    Infer declared match type from a conventional token in the name, e.g.:
      "[broad] shoes"  -> MatchType.BROAD
      "[phrase] hats"  -> MatchType.PHRASE
      "[exact] 'widgets'" -> MatchType.EXACT
    Returns None if no token is present.
    """
    n = norm(name)
    for tok, mtype in _TOKEN_TO_TYPE.items():
        if tok in n:
            return mtype
    return None

def expected_label(name: str) -> str | None:
    """
    Return the expected label token (e.g., "[broad]") based on declared_type(name).
    Returns None if no declared type is found.
    """
    mtype = declared_type(name)
    return _TYPE_TO_TOKEN.get(mtype) if mtype else None

def is_branded_search_name(name: str) -> bool:
    n = norm(name)
    return any(tok in n for tok in _BRAND_TOKENS)

def is_dynamic_search(name: str) -> bool:
    n = norm(name)
    return "dsa" in n or "dynamic search" in n

# Alias to satisfy core/__init__.py import
def is_dynamic_search_name(name: str) -> bool:
    return is_dynamic_search(name)

__all__ = [
    "MatchType",
    "has_match_type_token",
    "declared_type",
    "expected_label",
    "is_branded_search_name",
    "is_dynamic_search",
    "is_dynamic_search_name",
]
