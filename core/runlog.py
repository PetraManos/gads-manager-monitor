from dataclasses import dataclass
from typing import Any, Callable
from core.text import collapse_one_line

@dataclass
class RunLogCtx:
    customer_id: str
    check: str
    message: str
    extras: dict[str, Any] | None = None

    def one_line(self) -> str:
        base = f"[{self.check}] {collapse_one_line(self.message)}"
        if self.extras:
            return base + " " + collapse_one_line(str(self.extras))
        return base

class RunLogger:
    def __init__(self, writer: Callable[[RunLogCtx], None]):
        self._writer = writer
    def write(self, ctx: RunLogCtx) -> None:
        self._writer(ctx)

stdout_logger = RunLogger(lambda ctx: print(ctx.one_line()))
