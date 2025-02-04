from f_core.mods.type.main_ import Any

def subclass_(x: type, y: type) -> bool:
    return issubclass(x, y)

def instance_(x: Any(), y: type) -> bool:
    return isinstance(x, y)
