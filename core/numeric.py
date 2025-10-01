from decimal import Decimal

def as_number(x: object) -> float | None:
    if x is None:
        return None
    try:
        return float(str(x).replace(",", "").replace("%", ""))
    except Exception:
        return None

def to_currency(x: float | Decimal | int, symbol: str = "$", places: int = 2) -> str:
    try:
        return f"{symbol}{float(x):,.{places}f}"
    except Exception:
        return f"{symbol}0.00"
