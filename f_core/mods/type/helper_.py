import inspect
from typing import get_type_hints
from f_core.mods.type.op_ import prod_type_


def runtime_domain(func):
    def wrapper(*args, **kwargs):
        types_at_runtime = tuple(type(arg) for arg in args)
        return prod_type_(*types_at_runtime)
    return wrapper

def runtime_codomain(func):
    signature = inspect.signature(func)
    return_annotation = signature.return_annotation
    if return_annotation is not inspect.Signature.empty:
        return return_annotation
    return type(None)

def hinted_domain(func):
    type_hints = get_type_hints(func)
    if not type_hints:
        return type(None)
    domain_hints = [type_hints[param] for param in inspect.signature(func).parameters if param in type_hints]
    if len(domain_hints) == 1:
        return domain_hints[0]
    elif domain_hints:
        return prod_type_(*domain_hints)
    return type(None)

def hinted_codomain(func):
    type_hints = get_type_hints(func)
    if 'return' in type_hints:
        return type_hints['return']
    return type(None)

def check_domain(func, param_names, expected_types, actual_types):
    mismatches = [
        f"\n   - '{name}': should be '{expected.__name__}', but got '{actual.__name__}'"
        for name, expected, actual in zip(param_names, expected_types, actual_types)
        if expected != actual
    ]
    if mismatches:
        mismatch_str = "".join(mismatches)+"."
        raise TypeError(f"Domain mismatch in func '{func.__name__}': {mismatch_str}")

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

