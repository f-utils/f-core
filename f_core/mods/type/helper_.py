import inspect
from typing import get_type_hints
from f import f

def flat_(*types):
    if not types:
        return (), None
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

def prod_(*types):
    flat_types = flat_(*types)[0]
    is_flexible = flat_(*types)[1]

    if len(flat_types) == 0:
        return type(None)
    elif len(flat_types) == 1 and not is_flexible:
        return flat_types[0]

    class _prod(type):
        _types = flat_types
        def __instancecheck__(cls, instance):
            if not isinstance(instance, tuple):
                return False
            if not is_flexible:
                if len(instance) != len(flat_types):
                    return False

            if is_flexible:
                for typ in (type(x) for x in instance):
                    if not typ in flat_types:
                        return False
                return True
            return all(isinstance(elem, typ) for elem, typ in zip(instance, flat_types))

        def __iter__(cls):
            return iter(flat_types)

    if is_flexible:
        class_name = f"prod_[{', '.join(t.__name__ for t in flat_types)}]"
    else:
        class_name = f"prod_({', '.join(t.__name__ for t in flat_types)})"
    prod_ = _prod(class_name, (), {})

    return prod_

def runtime_domain(func):
    def wrapper(*args, **kwargs):
        types_at_runtime = tuple(type(arg) for arg in args)
        return prod_(*types_at_runtime)
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
    return tuple(type_hints[param] for param in func.__code__.co_varnames if param in type_hints) 

def hinted_codomain(func):
    type_hints = get_type_hints(func)
    return type_hints.get('return', type(None))

def extract_component_types(expected_type):
    """Extracts component types as a list from expected_type's __types__ attribute."""
    try:
        return getattr(expected_type, '__types__', [])
    except AttributeError:
        return []

def check_domain(func, param_names, expected_domain, actual_domain, args):
    mismatches = []
    for name, expected, actual in zip(param_names, expected_domain, actual_domain):
        expected_name = getattr(expected, '__name__', repr(expected))
        actual_name = getattr(actual, '__name__', repr(actual))
        if expected != actual:
            matched = False
            component_types = extract_component_types(expected)
            for op_name, op_data in f.op.E().items():
                op_func = op_data['op']['func']
                if expected.__name__ == op_func(*component_types).__name__:
                    matched = True
                    if issubclass(expected, actual) and hasattr(expected, 'check'):
                        actual_value = args[param_names.index(name)]
                        if not expected.check(actual_value):
                            raise TypeError(
                                f"Domain check failed in func '{func.__name__}':"
                                f"\n\t --> '{name}': expected type '{expected_name}' did not match "
                                f"the actual value '{actual_value}'."
                            )
                    break
            if not matched:
                mismatches.append(f"\n\t --> '{name}': should be '{expected_name}', but got '{actual_name}'")
    if mismatches:
        mismatch_str = "".join(mismatches) + "."
        raise TypeError(f"Domain mismatch in func '{func.__name__}': {mismatch_str}")

def check_codomain(func, expected_codomain, actual_codomain):
    """
    Compare the expected and actual codomain types. If there's a mismatch,
    raise a TypeError with a detailed message.
    """
    if type(actual_codomain) is type and type(expected_codomain) is type:
        if not issubclass(actual_codomain, expected_codomain):
            raise TypeError(
                f"Codomain mismatch in func '{func.__name__}': expected '{expected_codomain.__name__}', "
                f" got '{actual_codomain.__name__}'."
            )
    elif type(actual_codomain) is list and type(expected_codomain) is list:
        if all(type(i) is type and type(j) is type for (i, j) in zip(actual_codomain, expected_codomain)):
            if not any(issubclass(i, j) for (i,j) in zip(actual_codomain, expected_codomain)):
                raise TypeError(
                    f"Codomain mismatch in func '{func.__name__}': expected '{expected_codomain}', "
                    f" got '{actual_codomain.__name__}'."
                )
        else:
            raise TypeError(f"All entries of actual '{actual_codomain}' and expected codomain '{expected_codomain}' must be types.")
    elif type(actual_codomain) is type and type(expected_codomain) is list:
        if all(type(i) is type for i in expected_codomain):
            if not any(issubclass(actual_codomain, i) for i in expected_codomain):
                raise TypeError(
                    f"Codomain mismatch in func '{func.__name__}': expected '{expected_codomain.__name__}', "
                    f" got '{actual_codomain.__name__}'."
                )
        else:
            raise TypeError(f"All entries of expected codomain '{expected_codomain.__name__}' must be types.")
    else:
        raise TypeError(f"Both actual domain '{actual_codomain.__name__}' and expected domain '{expected_codomain.__name__}' must be types or '{expected_codomain.__name__}'  must be a list of types.")
