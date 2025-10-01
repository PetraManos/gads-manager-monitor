from __future__ import annotations
import re

def norm(s: object) -> str:
    return str(s or "").lower().replace("\u00A0", " ").strip()

def collapse_one_line(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def has_word(s: str, word: str) -> bool:
    s_l = (s or "").lower()
    w = re.escape((word or "").lower())
    return re.search(rf"(^|\W){w}(?=$|\W)", s_l) is not None
