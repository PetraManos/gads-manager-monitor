from __future__ import annotations
from typing import Optional
import re

def declared_type(name: str) -> Optional[str]:
    """
    BROAD_ONLY | PHRASE_ONLY | EXACT_ONLY | PHRASE_AND_EXACT | None
    """
    raw = (str(name or "")
           .lower()
           .replace("\xa0", " ")
           .replace("\u00a0", " "))
    n = f" {raw} "
    has_pe_abbrev = re.search(r'(^|[\s\-(_/\[])(p\s*[/+&]\s*e|e\s*[/+&]\s*p)([\s\-)/\]_]|\b|$)', n) is not None
    is_broad  = re.search(r'(^|[\s\-(_/\[])(broad|bm)([\s\-)/\]_]|\b|$)', n) is not None
    is_phrase = re.search(r'(^|[\s\-(_/\[])(phrase|pm)([\s\-)/\]_]|\b|$)', n) is not None
    is_exact  = re.search(r'(^|[\s\-(_/\[])(exact|em)([\s\-)/\]_]|\b|$)', n) is not None
    has_pe_words = re.search(r'(phrase\s*[/+&]\s*exact|exact\s*[/+&]\s*phrase)', n) is not None
    is_phrase_and_exact = has_pe_words or has_pe_abbrev or (is_phrase and is_exact)

    if is_phrase_and_exact and not is_broad: return "PHRASE_AND_EXACT"
    if is_broad and not is_phrase and not is_exact: return "BROAD_ONLY"
    if is_phrase and not is_broad and not is_exact: return "PHRASE_ONLY"
    if is_exact and not is_broad and not is_phrase: return "EXACT_ONLY"
    return None

def expected_label(decl: Optional[str]) -> str:
    if decl == "BROAD_ONLY": return "BROAD"
    if decl == "PHRASE_ONLY": return "PHRASE"
    if decl == "EXACT_ONLY":  return "EXACT"
    if decl == "PHRASE_AND_EXACT": return "PHRASE or EXACT"
    return ""

def has_match_type_token(name: str) -> bool:
    s = str(name or "").lower()
    return re.search(r"\b(?:exact|phrase|broad)\b[\s\-_]*\bmatch\b", s) is not None

def is_dynamic_search_name(name: str, subtype: Optional[str] = None) -> bool:
    return bool(re.search(r"\bdynamic\b", str(name or ""), re.I) or
                re.search(r"SEARCH_DYNAMIC_ADS", str(subtype or ""), re.I))

def is_branded_search_name(name: str) -> bool:
    return re.search(r"\bbrand(?:ed)?\b", str(name or ""), re.I) is not None
