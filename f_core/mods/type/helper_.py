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

def is_domain_hinted(func):
    type_hints = get_type_hints(func)
    param_hints = {param: type_hints.get(param) for param in inspect.signature(func).parameters}
    non_hinted_params = [param for param, hint in param_hints.items() if hint is None]
    if non_hinted_params:
        raise TypeError(
            f"Function '{func.__name__}' must have type hints for all parameters."
            f"\n\t --> Missing hints: '{', '.join(non_hinted_params)}'."
        )
    return True

def is_codomain_hinted(func):
    """Check if the function has a type hint for its return value and report if missing."""
    type_hints = get_type_hints(func)
    if 'return' not in type_hints or type_hints['return'] is None:
        raise TypeError(f"Function '{func.__name__}' must have a return type hint.")
    return True

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

def check_domain(func, param_names, expected_domain, actual_domain):
    mismatches = [
        f"\n\t --> '{name}': should be '{expected.__name__}', but got '{actual.__name__}'"
        for name, expected, actual in zip(param_names, expected_domain, actual_domain)
        if expected != actual
    ]
    if mismatches:
        mismatch_str = "".join(mismatches)+"."
        raise TypeError(f"Domain mismatch in func '{func.__name__}': {mismatch_str}")

def check_codomain(func, expected_codomain, actual_codomain):
    """
    Compare the expected and actual codomain types. If there's a mismatch,
    raise a TypeError with a detailed message.
    """
    if not issubclass(actual_codomain, expected_codomain):
        raise TypeError(
            f"Codomain mismatch in func '{func.__name__}': expected '{expected_codomain.__name__}', "
            f" got '{actual_codomain.__name__}'."
        )



