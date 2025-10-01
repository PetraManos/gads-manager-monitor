from typing import Dict
from core.violations.base import AccountCheck

class Registry:
    def __init__(self):
        self._checks: Dict[str, AccountCheck] = {}
    def register(self, check: AccountCheck) -> None:
        key = check.code
        if key in self._checks:
            raise ValueError(f"Duplicate violation code: {key}")
        self._checks[key] = check
    def list(self) -> list[str]:
        return sorted(self._checks.keys())
    def get(self, code: str) -> AccountCheck:
        return self._checks[code]

registry = Registry()

def register(check: AccountCheck) -> AccountCheck:
    registry.register(check)
    return check
