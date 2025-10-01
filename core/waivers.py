from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Iterable

class WaiverStatus(str, Enum):
    NONE = "NONE"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"

@dataclass
class WaiverKey:
    client: str
    code: str

@dataclass
class Waiver:
    key: WaiverKey
    status: WaiverStatus
    notes: str | None = None

class WaiverIndex:
    """In-memory index keyed by (client, code)."""
    def __init__(self):
        self._data: dict[tuple[str, str], Waiver] = {}
    def get(self, client: str, code: str) -> Waiver | None:
        return self._data.get((client, code))
    def upsert(self, waiver: Waiver) -> None:
        self._data[(waiver.key.client, waiver.key.code)] = waiver
    def status_for(self, client: str, code: str) -> WaiverStatus:
        w = self.get(client, code)
        return w.status if w else WaiverStatus.NONE

# -------- New: compatibility API expected by core/__init__.py --------

@dataclass
class WaiverRecord:
    """Row-like waiver input used to build the index."""
    client: str
    code: str
    status: str = "ACTIVE"  # accepts raw strings; mapped to WaiverStatus
    notes: str | None = None

def _to_status(s: str | WaiverStatus | None) -> WaiverStatus:
    if isinstance(s, WaiverStatus):
        return s
    s_norm = (s or "NONE").strip().upper()
    return WaiverStatus[s_norm] if s_norm in WaiverStatus.__members__ else WaiverStatus.NONE

def build_waivers_index(records: Iterable[WaiverRecord]) -> WaiverIndex:
    """
    Convert an iterable of WaiverRecord to a WaiverIndex keyed by (client, code).
    Later we can swap this out for a Sheet-backed implementation.
    """
    idx = WaiverIndex()
    for r in records or []:
        idx.upsert(Waiver(WaiverKey(r.client, r.code), _to_status(r.status), r.notes))
    return idx

def get_waiver_status_from_index(index: WaiverIndex, client: str, code: str) -> WaiverStatus:
    """Helper used by checks to query status without knowing index internals."""
    return index.status_for(client, code)

__all__ = [
    "WaiverStatus",
    "WaiverKey",
    "Waiver",
    "WaiverIndex",
    "WaiverRecord",
    "build_waivers_index",
    "get_waiver_status_from_index",
]
