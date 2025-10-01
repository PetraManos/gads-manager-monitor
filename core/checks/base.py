from dataclasses import dataclass
from typing import Any, Optional
from .registry import registry

@dataclass
class Result:
    ok: bool
    summary: str
    details: Optional[Any] = None
    code: str = ""
    customer_id: str = ""

class BaseCheck:
    code: str = ""
    description: str = ""
    def run(self, provider, customer_id: str) -> 'Result':
        raise NotImplementedError

# Back-compat aliases / helpers:
Check = BaseCheck

def register(check_cls):
    return registry.register(check_cls)

def list_codes():
    return registry.list()
