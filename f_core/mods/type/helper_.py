from typing import get_type_hints


def flat_(*types):
    if not types:
        return None
    for typ in types:
        if not isinstance(typ, type) and not isinstance(typ, list):
            raise TypeError(f"{typ} is not a valid type.")
    is_flexible = False
    flat_types = ()

    if len(types) == 1 and isinstance(types[0], list):
        is_flexible = True
        flat_types = tuple(types[0])
    else:
        flat_types = types

    return (flat_types, is_flexible)

def func_instance_(instance, flat_types, is_flexible, cod=None):
    if not isinstance(instance, TypedFunc):
        try:
            instance = TypedFunc(instance)
        except:
            return False
    if not callable(instance):
        return False

    type_hints = get_type_hints(instance.func)
    domain_hints = tuple(type_hints.values())[:-1]
    if cod:
        return_hint = tuple(type_hints.values())[-1]
        if not return_hint == cod:
            return False

    if is_flexible:
        for x in domain_hints:
            if not x in flat_types:
                return False
        return True
    return domain_hints == flat_types


