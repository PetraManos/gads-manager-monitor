# core/names.py
from __future__ import annotations
import re
from typing import Optional
from core.string_utils import norm  # single source of truth

_SEP_RX = re.compile(r"[-_/+&]")              # normalize separators to spaces
_WORD_RX = re.compile(r"[a-z]+")              # letter tokens
_PE_RX   = re.compile(r"\b(p\s*[/+&]\s*e|e\s*[/+&]\s*p)\b", re.I)

# GS-parity: require "... match" with exact|phrase|broad.
# Use alphabet-only boundaries so underscores/hyphens count as separators.
_MATCH_TOKEN_RX = re.compile(
    r"(?<![a-z])(?:exact|phrase|broad)(?![a-z])[\s\-_]*"
    r"(?<![a-z])match(?![a-z])",
    re.I,
)


def _tokens_from_normalized(n: str) -> set[str]:
    s = _SEP_RX.sub(" ", n)
    return set(_WORD_RX.findall(s))

class CampaignName:
    """
    Encapsulates campaign naming classification.

    Example:
        campaign_name = CampaignName("Brand - Phrase")
        campaign_name.declared_type        -> "PHRASE_ONLY"
        campaign_name.expected_label       -> "PHRASE"
        campaign_name.has_match_type_token -> True
        campaign_name.is_dynamic_search    -> False
        campaign_name.is_branded_search    -> True
    """
    __slots__ = ("raw", "n", "_toks")

    def __init__(self, raw: str):
        self.raw = raw or ""
        self.n = norm(self.raw)              # lowercase, NBSP→space, collapse ws
        self._toks = _tokens_from_normalized(self.n)

    @property
    def tokens(self) -> set[str]:
        return self._toks

    @property
    def has_match_type_token(self) -> bool:
        return _MATCH_TOKEN_RX.search(self.n) is not None

    @property
    def declared_type(self) -> Optional[str]:
        toks = self._toks
        # Shorthand like "p/e" or both tokens present
        if _PE_RX.search(self.n) or ({"phrase", "exact"} <= toks):
            return "PHRASE_AND_EXACT"
        if "phrase" in toks and not {"exact", "broad"} & toks:
            return "PHRASE_ONLY"
        if "exact" in toks and not {"phrase", "broad"} & toks:
            return "EXACT_ONLY"
        if "broad" in toks and not {"phrase", "exact"} & toks:
            return "BROAD_ONLY"
        return None

    @property
    def expected_label(self) -> str:
        mapping = {
            "PHRASE_ONLY": "PHRASE",
            "EXACT_ONLY": "EXACT",
            "BROAD_ONLY": "BROAD",
            "PHRASE_AND_EXACT": "PHRASE or EXACT",
        }
        return mapping.get(self.declared_type or "", "")

    @property
    def is_dynamic_search(self) -> bool:
        # matches 'dynamic', 'dynamicsearch', or 'dsa'
        return bool(
            "dynamic" in self._toks
            or "dynamicsearch" in self._toks
            or re.search(r"\bdsa\b", self.n)
        )

    @property
    def is_branded_search(self) -> bool:
        # treat both "brand" and "branded" as branded
        return re.search(r"\bbrand(?:ed)?\b", self.n) is not None


# ---- Optional thin wrappers (safe to remove after migrating call sites) ----
def has_match_type_token(name: str) -> bool:
    return CampaignName(name).has_match_type_token

def declared_type(name: str) -> Optional[str]:
    return CampaignName(name).declared_type

def expected_label(declared: Optional[str]) -> str:
    mapping = {
        "PHRASE_ONLY": "PHRASE",
        "EXACT_ONLY": "EXACT",
        "BROAD_ONLY": "BROAD",
        "PHRASE_AND_EXACT": "PHRASE or EXACT",
    }
    return mapping.get(declared or "", "")

def is_dynamic_search_name(name: str) -> bool:
    return CampaignName(name).is_dynamic_search

def is_branded_search_name(name: str) -> bool:
    return CampaignName(name).is_branded_search


__all__ = [
    "CampaignName",
    # wrappers:
    "has_match_type_token",
    "declared_type",
    "expected_label",
    "is_dynamic_search_name",
    "is_branded_search_name",
]
