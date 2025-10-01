from enum import Enum
from core.text import norm

class MatchType(str, Enum):
    BROAD = "BROAD"
    PHRASE = "PHRASE"
    EXACT = "EXACT"

_BRAND_TOKENS = {"brand", "branded"}

def has_match_type_token(name: str) -> bool:
    n = norm(name)
    return any(t in n for t in ("[broad]", "[phrase]", "[exact]"))

def is_branded_search_name(name: str) -> bool:
    n = norm(name)
    return any(tok in n for tok in _BRAND_TOKENS)

def is_dynamic_search(name: str) -> bool:
    n = norm(name)
    return "dsa" in n or "dynamic search" in n
