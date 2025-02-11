from f_core.mods.type.helper_ import (
    flat_,
    hinted_domain,
    hinted_codomain
)
from f_core.mods.type.func_ import (
    HintedDomFunc,
    HintedCodFunc,
    HintedFunc,
    TypedDomFunc,
    TypedCodFunc,
    TypedFunc,
    BooleanFunc
)

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
