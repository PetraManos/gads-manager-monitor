class _Registry:
    def __init__(self):
        self._items = {}

    def register(self, check_cls):
        inst = check_cls()
        self._items[inst.code] = inst
        return check_cls

    def get(self, code):
        return self._items.get(code)

    def list(self):
        return sorted(self._items.keys())

registry = _Registry()
