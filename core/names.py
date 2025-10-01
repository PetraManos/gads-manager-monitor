import re
from typing import Optional

# --- helpers -----------------------------------------------------------------

def _norm(s: str) -> str:
    """Lowercase, normalize NBSPs, collapse whitespace."""
    t = (s or "").replace("\xa0", " ").replace("\u00a0", " ").lower()
    return " ".join(t.split())

def _tokens(s: str) -> set[str]:
    """Word tokens (letters only) after normalizing common separators."""
    s = _norm(s)
    # Turn separators into spaces so "Brand - Phrase", "Phrase/Exact" tokenize well
    s = re.sub(r"[-_/+&]", " ", s)
    return set(re.findall(r"[a-z]+", s))

# --- public API ---------------------------------------------------------------

def has_match_type_token(name: str) -> bool:
    """True if the string mentions phrase/exact/broad (or P/E shorthand)."""
    n = _norm(name)
    toks = _tokens(n)
    if {"phrase", "exact"} & toks or "broad" in toks:
        return True
    # Allow shorthand like "p/e" or "e/p"
    if re.search(r"\bp\s*/\s*e\b|\be\s*/\s*p\b", n):
        return True
    return False

def declared_type(name: str) -> Optional[str]:
    """
    Map a human label to an internal declared type:
      - 'Brand - Phrase' -> 'PHRASE_ONLY'
      - 'Brand - Exact'  -> 'EXACT_ONLY'
      - 'Brand - Broad'  -> 'BROAD_ONLY'
      - 'P/E' or 'Phrase & Exact' -> 'PHRASE_AND_EXACT'
      - otherwise -> None
    """
    n = _norm(name)
    toks = _tokens(n)

    # Shorthand like "p/e" or "e/p"
    if re.search(r"\bp\s*/\s*e\b|\be\s*/\s*p\b", n) or ({"phrase", "exact"} <= toks):
        return "PHRASE_AND_EXACT"

    if "phrase" in toks:
        return "PHRASE_ONLY"
    if "exact" in toks:
        return "EXACT_ONLY"
    if "broad" in toks:
        return "BROAD_ONLY"

    return None

def expected_label(declared: Optional[str]) -> str:
    """
    Human-facing label for a declared type, used in UI/reports/tests.
    """
    mapping = {
        "PHRASE_ONLY": "PHRASE",
        "EXACT_ONLY": "EXACT",
        "BROAD_ONLY": "BROAD",
        "PHRASE_AND_EXACT": "PHRASE or EXACT",
    }
    return mapping.get(declared or "", "")

def is_dynamic_search_name(name: str) -> bool:
    """
    True if the name indicates Dynamic Search (e.g., contains 'dynamic' or 'dsa').
    """
    toks = _tokens(name)
    return "dynamic" in toks or "dsa" in toks or "dynamicsearch" in toks

def is_branded_search_name(name: str) -> bool:
    """
    True if the name looks like a branded segment (contains 'brand' token).
    """
    return "brand" in _tokens(name)

__all__ = [
    "has_match_type_token",
    "declared_type",
    "expected_label",
    "is_dynamic_search_name",
    "is_branded_search_name",
]
