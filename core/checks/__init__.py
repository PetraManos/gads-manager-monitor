# Auto-load example checks so their @register runs during imports (incl. tests)
from . import examples as _examples  # noqa: F401
