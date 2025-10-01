from dataclasses import dataclass
from typing import Any, Optional

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

    def run(self, provider, customer_id: str) -> Result:
        raise NotImplementedError
