from dataclasses import dataclass
from typing import Protocol, Any

@dataclass
class ViolationResult:
    violated: bool
    details: dict[str, Any] | None = None

class AccountCheck(Protocol):
    code: str
    description: str
    def run(self, customer_id: str, **params) -> ViolationResult: ...

class EntityCheck(Protocol):
    code: str
    description: str
    def run(self, customer_id: str, entity_id: str, **params) -> ViolationResult: ...
