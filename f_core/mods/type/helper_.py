import inspect
from typing import get_type_hints
from f_core.mods.type.op_ import prod_type_


def runtime_domain(func):
    signature = inspect.signature(func)
    domain_types = tuple(param.annotation for param in signature.parameters.values() if param.annotation is not param.empty)
    if domain_types:
        return prod_type_(*domain_types)
    return type(None)

def runtime_codomain(func):
    signature = inspect.signature(func)
    return_annotation = signature.return_annotation
    if return_annotation is not inspect.Signature.empty:
        return return_annotation
    return type(None)

def hinted_domain(func):
    type_hints = get_type_hints(func)
    domain_hints = tuple(type_hints.values())[:-1]
    if domain_hints:
        return prod_type_(*domain_hints)
    return type(None)

def hinted_codomain(func):
    type_hints = get_type_hints(func)
    return_hint = tuple(type_hints.values())[-1]
    if return_hint:
        return return_hint
    return type(None)

def check_domain(func):
    signature = inspect.signature(func)
    param_names = list(signature.parameters.keys())
    runtime_dom = runtime_domain(func)
    hinted_dom = hinted_domain(func)

    if runtime_dom != hinted_dom:
        mismatches = [
            (name, rt, ht) for name, rt, ht in zip(param_names, runtime_dom, hinted_dom)
            if rt != ht
        ]
        mismatch_str = "\n> ".join(
            f"'{name}': received '{rt.__name__}' while expecting '{ht.__name__}'."
            for name, rt, ht in mismatches
        )
        raise TypeError(
            f"Function '{func.__name__}': Runtime domain does not match hinted domain. Mismatches:\n {mismatch_str}"
        )
    return True

def check_codomain(func):
    runtime_cod = runtime_codomain(func)
    hinted_cod = hinted_codomain(func)

    if runtime_cod != hinted_cod:
        raise TypeError(
            f"Function '{func.__name__}': Runtime codomain '{runtime_cod.__name__}' does not match hinted codomain '{hinted_cod.__name__}'."
        )
    return True

def hinted_comp(f, g):
    if not issubclass(hinted_codomain(f.func), hinted_domain(g.func)):
        raise TypeError(f"Hinted codomain '{hinted_codomain(f.func).__name__}' of '{f.__name__}' does not match hinted domain '{hinted_domain(g.func).__name__}' of '{g.__name__}'.")
    return lambda *args, **kwargs: g.func(f.func(*args, **kwargs))

def runtime_comp(f, g):
    if not issubclass(runtime_codomain(f.func), runtime_domain(g.func)):
        raise TypeError(f"Runtime codomain '{runtime_codomain(f.func).__name__}' of '{f.__name__}' does not match runtime domain '{runtime_domain(g.func).__name__}' of '{g.__name__}'.")
    return lambda *args, **kwargs: g.func(f.func(*args, **kwargs))

def typed_comp(f, g):
    if not issubclass(f.codomain, g.domain):
        raise TypeError(f"Typed codomain of 'f' does not match typed domain of 'g'.")
    return lambda *args, **kwargs: g.func(f.func(*args, **kwargs))


def flat_(*types):
    if not types:
        return None
    for typ in types:
        if not isinstance(typ, type) and not isinstance(typ, list):
            raise TypeError(f"{typ.__name__} is not a valid type.")
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
