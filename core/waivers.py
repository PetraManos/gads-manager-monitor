from enum import Enum
from dataclasses import dataclass

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
    def __init__(self):
        self._data: dict[tuple[str, str], Waiver] = {}
    def get(self, client: str, code: str) -> Waiver | None:
        return self._data.get((client, code))
    def upsert(self, waiver: Waiver) -> None:
        self._data[(waiver.key.client, waiver.key.code)] = waiver
    def status_for(self, client: str, code: str) -> WaiverStatus:
        w = self.get(client, code); return w.status if w else WaiverStatus.NONE
