from f import f

from f_core.mods.type.helper_ import (
    flat_,
    prod_,
    hinted_domain,
    hinted_codomain
)
from f_core.mods.type.type_ import (
    HintedDomFunc,
    HintedCodFunc,
    HintedFunc,
    TypedDomFunc,
    TypedCodFunc,
    TypedFunc,
    BooleanFunc
)

# ----------------------
#    Type Operations
# ----------------------

def inter_type_(*types):
    """
    Build the 'intersection' of types:
        > an object 'p' of the inter_(X, Y, ...)
        > is an object of every 'X, Y, ...'
    """
    unique_types = list(set(types))
    if len(unique_types) == 1:
        return unique_types[0]
    if len(unique_types) == 0:
        return type(None)

    if any(t.__module__ == 'builtins' for t in unique_types):
        raise TypeError("Cannot create an intersection type with built-in types due to potential layout conflicts.")

    class_name = f"inter_({', '.join(t.__name__ for t in types)})"

    class _inter(*unique_types):
        __name__ = class_name
        def __instancecheck__(cls, instance):
            return all(isinstance(instance, t) for t in unique_types)

    _inter.__name__ = class_name

    return _inter


def coprod_type_(*types):
    """
    Build the 'coproduct' of types:
        > an object 'p' of the coproduct between 'X, Y, ...'
        > is an object of some of 'X, Y, ...'
    """
    flat_types = flat_(*types)[0]
    is_flexible = flat_(*types)[1]

    if len(flat_types) == 0:
        return type(None)
    elif len(flat_types) == 1 and not is_flexible:
       return flat_types[0]

    class _coprod(type):
        def __instancecheck__(cls, instance):
            if type(instance) not in flat_types:
                return False
            return True

    if is_flexible:
        class_name = f"coprod_[{', '.join(t.__name__ for t in flat_types)}]"
    else:
        class_name = f"coprod_({', '.join(t.__name__ for t in flat_types)})"
    coprod_ = _coprod(class_name, (), {})
    return coprod_

def prod_type_(*types):
    """
    Build the 'product' of types:
        > the objects of the product between 'X, Y, ...'
        > are the tuples '(x, y, ...)' such that
        > 'x, y, ...' are in 'X, Y, ...'
    """
    return prod_(*types)

def unprod_type_(*types):
    """
    Build the 'unordered product' of types:
        > the objects of the unproduct between 'X, Y, ...'
        > are the sets '{x, y, ...}' such that
        > 'tuple({x, y, ...})' is in 'prod_(X, Y, ...)'
    Flexible case:
        > the objects of 'unprod_([X, Y, ...])'
        > are sets '{x, y, ...}' with any number of elements
        > such that 'x, y, ...' are in 'coprod_(X, Y, ...)'
    """
    flat_types, is_flexible = flat_(*types)

    class _unprod(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, set):
                return False

            if is_flexible:
                for elem in instance:
                    if not isinstance(elem, tuple(flat_types)):
                        return False
                return True

            if len(instance) != len(flat_types):
                return False

            type_counts = {typ: flat_types.count(typ) for typ in flat_types}
            for elem in instance:
                for typ in type_counts:
                    if isinstance(elem, typ) and type_counts[typ] > 0:
                        type_counts[typ] -= 1
                        break
                else:
                    return False
            return all(count == 0 for count in type_counts.values())

    if is_flexible:
        class_name = f"unprod_[{', '.join(t.__name__ for t in flat_types)}]"
    else:
        class_name = f"unprod_({', '.join(t.__name__ for t in flat_types)})"
    return _unprod(class_name, (), {})


def set_type_(*types):
    """
    Build the 'set product' of types:
        > the objects of 'setprod_(X, Y, ...)'
        > are the sets '{x, y, ...}' such that
        > 'len({x, y, ...})' is 'len((X, Y, ...))'
        > 'x, y, ...' are in 'coprod_(X, Y, ...)'
    Flexible case:
        > the objects of 'setprod_([X, Y, ...])'
        > are sets '{x, y, ...}' with any number of elements
        > such that 'x, y, ...' are in 'coprod_(X, Y, ...)'
    """
    flat_types, is_flexible = flat_(*types)

    class _set(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, set):
                return False
            if is_flexible:
                for elem in instance:
                    if not isinstance(elem, tuple(flat_types)):
                        return False
                return True
            if len(instance) != len(flat_types):
                return False
            type_counts = {typ: flat_types.count(typ) for typ in flat_types}
            for elem in instance:
                for typ in type_counts:
                    if isinstance(elem, typ) and type_counts[typ] > 0:
                        type_counts[typ] -= 1
                        break
                else:
                    return False
            return all(count == 0 for count in type_counts.values())

    if is_flexible:
        class_name = f"set_([{', '.join(t.__name__ for t in flat_types)}])"
    else:
        class_name = f"set_({', '.join(t.__name__ for t in flat_types)})"
    return _set(class_name, (), {})

def dict_type_(*types):
    """
    Build the 'dictionary product' of types:
        > the objects of the 'dict_({X0: X1, Y0: Y1, ...})'
        > are the dictionaries '{x0: x1, y0: y1, ...}' such that
        > have the same number of entries as '{X0: X1, Y0: Y1, ...}'
        > 'x0, y0, ...' are in 'X0, Y0, ...'
        > 'x1, y1, ...' are in 'X1, Y1, ...'
    Flexible case:
        > object of 'dict_({[X0, Y0, ...]: [X1, Y1, ...]})'
        > is any dictionary whose key have types in 'coprod_(X0, Y0, ...)'
        > and whose values have type in 'coprod_(X1, Y1, ...)'
    """
    if len(types) != 2:
        raise TypeError("Must provide both key and value types.")

    key_types, is_key_flexible = flat_(*types[0])
    value_types, is_value_flexible = flat_(*types[1])

    class _dict(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, dict):
                return False
            if is_key_flexible and is_value_flexible:
                for key, value in instance.items():
                    if not isinstance(key, tuple(key_types)) or not isinstance(value, tuple(value_types)):
                        return False
                return True

            if len(instance) != len(key_types) or len(instance) != len(value_types):
                return False
            key_count = {typ: key_types.count(typ) for typ in key_types}
            value_count = {typ: value_types.count(typ) for typ in value_types}

            for key, value in instance.items():
                key_matched = value_matched = False
                for key_type, value_type in zip(key_count, value_count):
                    if isinstance(key, key_type) and key_count[key_type] > 0:
                        key_count[key_type] -= 1
                        key_matched = True

                    if isinstance(value, value_type) and value_count[value_type] > 0:
                        value_count[value_type] -= 1
                        value_matched = True

                if not key_matched or not value_matched:
                    return False
            return all(count == 0 for count in key_count.values()) and all(count == 0 for count in value_count.values())

    class_name = f"dict_({{{', '.join(t.__name__ for t in key_types)}}}:{{{', '.join(t.__name__ for t in value_types)}}})"
    return _dict(class_name, (), {})


def hdfunc_type_(*domain_types):
    """
    Build the 'hinted-domain function type' of types:
        > the objects of 'hdfunc_type_(X, Y, ...)'
        > are objects 'f(x: X, y: Y, ...)' of 'HintedDomFunc'
    Flexible case:
        > objects of 'hdfunc_type_([X, Y, ...])'
        > are objects 'f(*args)' of 'HintedDomFunc'
        > whose arguments in the domain have type hints that
        > belong to 'coprod_(X, Y, ...)'
    """
    lat_types, is_flexible = flat_(*domain_types)

    class_name = "hdfunc_type_[" + (", ".join(t.__name__ for t in flat_types)) + "]"

    class _hdfunc(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, HintedDomFunc):
                return False

            domain_hints = set(hinted_domain(instance.func))

            if is_flexible:
                if not set(flat_types).issubset(domain_hints):
                    return False
            else:
                if domain_hints != set(flat_types):
                    return False

            return True

    return _hdfunc(class_name, (), {})

def hcfunc_type_(*codomain_types):
    """
    Build the 'hinted-codomain function type' of types:
        > the objects of hc_func_type_(R) are
        > objects 'f(x, y, ... ) -> R' of HintedCodFunc
    Flexible case:
        > objects of 'hcfunc_type_([R, S, ...])'
        > are objects 'f(*args)' of HintedCodFunc
        > whose return type hint belong to 'coprod_(R, S, ...)'
    """
    class_name = f"hcfunc_type_[cod={cod.__name__}]"

    class _hcfunc(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, HintedCodFunc):
                return False

            return_hint = hinted_codomain(instance.func)

            return return_hint == cod

    return _hcfunc(class_name, (), {})

def hfunc_type_(*domain_types, cod=None):
    """
    Build the 'hinted function type' of types:
        > the objects of hfunc_type(X, Y, ..., cod=R)
        > are objects 'f(x: X, y: Y, ...) -> R' of HintedFunc
    Flexible case:
        > objects of 'hfunc_type_([X, Y, ...], cod=[R, S, ...])'
        > are objects 'f(*args)' of HintedFunc
        > whose argument type hints belong to 'coprod_(X, Y, ...)'
        > and whose return type hint belongs to 'coprod_(R, S, ...)'
    """
    if cod is None:
        raise TypeError("Codomain type must be specified.")

    flat_types, is_flexible = flat_(*domain_types)

    class_name = "hfunc_type_[" + (", ".join(t.__name__ for t in flat_types)) + f"]; cod={cod.__name__}"

    class _hfunc(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, HintedFunc):
                return False

            domain_hints = set(hinted_domain(instance.func))
            return_hint = hinted_codomain(instance.func)

            if is_flexible:
                if not set(flat_types).issubset(domain_hints):
                    return False
            else:
                if domain_hints != set(flat_types):
                    return False

            return return_hint == cod

    return _hfunc(class_name, (), {})

def tdfunc_type_(*domain_types):
    """
    Build the 'typed-domain function type' of types:
        > the objects of 'tdfunc_type_(X, Y, ...)'
        > are objects 'f(x: X, y: Y, ...)' of 'TypedDomFunc'
    Flexible case:
        > objects of 'tdfunc_type_([X, Y, ...])'
        > are objects 'f(*args)' of 'TypedDomFunc'
        > whose arguments in the domain have type hints that
        > belong to 'coprod_(X, Y, ...)'
    """
    flat_types, is_flexible = flat_(*domain_types)

    class_name = "tdfunc_type_[" + (", ".join(t.__name__ for t in flat_types)) + "]"

    class _tdfunc(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, TypedDomFunc):
                return False

            domain_hints = set(hinted_domain(instance.func))

            if is_flexible:
                if not set(flat_types).issubset(domain_hints):
                    return False
            else:
                if domain_hints != set(flat_types):
                    return False

            return True

    return _tdfunc(class_name, (), {})

def tcfunc_type_(cod):
    """
    Build the 'typed-codomain function type' of types:
        > the objects of tc_func_type_(R) are
        > objects 'f(x, y, ... ) -> R' of TypedCodFunc
    Flexible case:
        > objects of 'tcfunc_type_([R, S, ...])'
        > are objects 'f(*args)' of TypedCodFunc
        > whose return type hint belong to 'coprod_(R, S, ...)'
    """
    class_name = f"tcfunc_type_[cod={cod.__name__}]"

    class _tcfunc(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, TypedCodFunc):
                return False

            return_hint = hinted_codomain(instance.func)

            return return_hint == cod

    return _tcfunc(class_name, (), {})


def tfunc_type_(*domain_types, cod=None):
    if cod is None:
        raise TypeError("Codomain type must be specified.")

    flat_types, is_flexible = flat_(*domain_types)

    class_name = "tfunc_type_[" + (", ".join(t.__name__ for t in flat_types)) + f"]; cod={cod.__name__}"

    class _tfunc(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, TypedFunc):
                return False

            domain_hints = set(hinted_domain(instance.func))
            return_hint = hinted_codomain(instance.func)

            if is_flexible:
                if not set(flat_types).issubset(domain_hints):
                    return False
            else:
                if domain_hints != set(flat_types):
                    return False

            if return_hint != cod:
                return False

            return True

    return _tfunc(class_name, (), {})

def bfunc_type_(*domain_types):
    """
    Build the type of 'boolean functions' on a given type:
        > the objects of 'bfunc_(X, Y, ...)'  are
        > typed functions f(x: X, y: Y, ...) -> bool
    """
    flat_types, is_flexible = flat_(*domain_types)

    class_name = "bfunc_type_[" + (", ".join(t.__name__ for t in flat_types)) + "]"

    class _bfunc(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, BooleanFunc):
                return False

            domain_hints = set(hinted_domain(instance.func))
            return_hint = hinted_codomain(instance.func)

            if is_flexible:
                if not set(flat_types).issubset(domain_hints):
                    return False
            else:
                if domain_hints != set(flat_types):
                    return False

            if return_hint != bool:
                return False

            return True

    return _bfunc(class_name, (), {})

def sub_type_(parent, *funcs):
    """
    Build the subtype 'sub_type(X, *funcs)' of a 'parent' type such that:
    1. 'x' is an object only if  Each function in 'funcs' is a boolean function
       with the domain 'prod_([parent])'
    3. The subtype includes objects from 'parent' for
       which all functions return True
    """
    if not isinstance(parent, type):
        raise TypeError("Argument 'parent' must be a type.")

    def is_valid_func(func):
        actual_func = func.func if hasattr(func, 'func') else func
        return (callable(actual_func) and
                all(hint == parent for hint in hinted_domain(actual_func)) and
                hinted_codomain(actual_func) is bool)

    for f in funcs:
        if not is_valid_func(f):
            raise TypeError("Each function in 'funcs' must be a callable boolean function with domain 'prod_([parent])'.")

    class _sub(parent):
        def __init__(self, value):
            if not all(func.func(value) for func in funcs):
                raise ValueError("Object does not satisfy all conditions in the given funcs.")
            super().__init__()

        def __instancecheck__(cls, instance):
            return isinstance(instance, parent) and all(func.func(instance) for func in funcs)

    sub_class_name = f"sub_({parent.__name__})"
    return type(sub_class_name, (_sub,), {})

def compl_type_(parent, *subclasses):
    if not isinstance(parent, type):
        raise TypeError(f"'{parent}' is not a type.")
    mistake_subclasses = []
    for subclass in subclasses:
        if not issubclass(subclass, parent):
            mistake_subclasses.append(subclass)
    if mistake_subclasses:
        raise TypeError(f"'{missing_subclasses}' are not a subtypes of '{parent}'.")
    class ComplementType(parent):
        def __new__(cls, value, *args, **kwargs):
            mistake_values = []
            mistake_subclasses = []
            for subclass in subclasses:
                if callable(subclass):
                    try:
                        if subclass(value):
                            mistake_subclasses.append(subclass.__name__)
                            mistake_values.append(value)
                    except:
                        return super(ComplementType, cls).__new__(cls, value, *args, **kwargs)
            if mistake_values and mistake_subclasses:
                raise TypeError(f"'{mistake_values}' is instance of the corresponding subtype '{mistake_subclasses}'")
        def __init__(self, value, *args, **kwargs):
            super().__init__()

        @classmethod
        def __instancecheck__(cls, instance):
            return isinstance(instance, ComplementType) and not any(isinstance(instance.value, subclass) for subclass in subclasses) 

    return ComplementType
