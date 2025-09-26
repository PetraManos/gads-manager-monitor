from __future__ import annotations
from typing import Any, Iterable, Iterator, List
import re

def norm(s: Any) -> str:
    return str(s or "").lower().replace("\u00A0"," ").replace("\xa0"," ").strip()

def norm_collapse(s: Any) -> str:
    return re.sub(r"\s+", " ", norm(s))

def make_key(client_name: str, code: str) -> str:
    return f"{norm_collapse(client_name)}|{norm_collapse(code)}"

def has_word(text: str, word: str) -> bool:
    rx = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
    return bool(rx.search(str(text or "")))

def chunks(iterable: Iterable[Any], size: int) -> Iterator[List[Any]]:
    assert size > 0
    buf: List[Any] = []
    for x in iterable:
        buf.append(x)
        if len(buf) >= size:
            yield buf; buf = []
    if buf: yield buf

def find_col_eq(headers: List[Any], name: str) -> int:
    tgt = str(name).lower()
    for i, h in enumerate(headers):
        if str(h).lower() == tgt:
            return i
    return -1
