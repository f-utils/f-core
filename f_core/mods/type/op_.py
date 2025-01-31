class Helper:
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

def coprod_type_(*types):
    """
    Build the 'coproduct' of types:
        > an object 'p' of the coproduct between 'X, Y, ...'
        > is an object of some of 'X, Y, ...'
    """
    flat_types = Helper.flat_(*types)[0]
    is_flexible = Helper.flat_(*types)[1]

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
    flat_types = Helper.flat_(*types)[0]
    is_flexible = Helper.flat_(*types)[1]

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
    flat_types, is_flexible = Helper.flat_(*types)

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
    flat_types, is_flexible = Helper.flat_(*types)

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

    key_types, is_key_flexible = Helper.flat_(*types[0])
    value_types, is_value_flexible = Helper.flat_(*types[1])

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
    flat_types, is_flexible = Helper.flat_(*domain_types)

    class _hdfunc(HintedDomFunc):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, HintedDomFunc):
                return False

            domain_hints = hinted_domain(instance.func)

            if is_flexible:
                return all(hint in flat_types for hint in domain_hints)
            return domain_hints == flat_types

    class_name = f"hdfunc_({{{', '.join(t.__name__ for t in flat_types)}}})"
    return type(class_name, (_hdfunc,), {})

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
    flat_types, is_flexible = Helper.flat_(*codomain_types)

    class _hcfunc(HintedCodFunc):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, HintedCodFunc):
                return False

            return_type = hinted_codomain(instance.func)

            if is_flexible:
                return return_type in flat_types
            return return_type == flat_types[0]

    class_name = f"hcfunc_({{{', '.join(t.__name__ for t in flat_types)}}})"
    return type(class_name, (_hcfunc,), {})

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

    flat_domain_types, domain_is_flexible = Helper.flat_(*domain_types)
    flat_codomain_types, codomain_is_flexible = Helper.flat_(cod)

    class _hfunc(HintedFunc):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, HintedFunc):
                return False

            domain_hints = hinted_domain(instance.func)
            return_type = hinted_codomain(instance.func)

            domain_check = (
                all(hint in flat_domain_types for hint in domain_hints)
                if domain_is_flexible else
                domain_hints == flat_domain_types
            )

            codomain_check = (
                return_type in flat_codomain_types
                if codomain_is_flexible else
                return_type == flat_codomain_types[0]
            )

            return domain_check and codomain_check

    class_name = (
        f"hfunc_({{{', '.join(t.__name__ for t in flat_domain_types)}}};"
        f" cod={{{', '.join(t.__name__ for t in flat_codomain_types)}}})"
    )
    return type(class_name, (_hfunc,), {})

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
    flat_types, is_flexible = Helper.flat_(*domain_types)

    class _tdfunc(TypedDomFunc):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, TypedDomFunc):
                return False

            domain_hints = hinted_domain(instance.func)

            if is_flexible:
                return all(hint in flat_types for hint in domain_hints)
            return domain_hints == flat_types

    class_name = f"tdfunc_({{{', '.join(t.__name__ for t in flat_types)}}})"
    return type(class_name, (_tdfunc,), {})

def tcfunc_type_(*codomain_types):
    """
    Build the 'typed-codomain function type' of types:
        > the objects of tc_func_type_(R) are
        > objects 'f(x, y, ... ) -> R' of TypedCodFunc
    Flexible case:
        > objects of 'tcfunc_type_([R, S, ...])'
        > are objects 'f(*args)' of TypedCodFunc
        > whose return type hint belong to 'coprod_(R, S, ...)'
    """
    flat_types, is_flexible = Helper.flat_(*codomain_types)

    class _tcfunc(TypedCodFunc):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, TypedCodFunc):
                return False

            return_type = hinted_codomain(instance.func)

            if is_flexible:
                return return_type in flat_types
            return return_type == flat_types[0]

    class_name = f"tcfunc_({{{', '.join(t.__name__ for t in flat_types)}}})"
    return type(class_name, (_tcfunc,), {})

def tfunc_type_(*domain_types, cod=None):
    """
    Build the 'typed function type' of types:
        > the objects of tfunc_type(X, Y, ..., cod=R)
        > are objects 'f(x: X, y: Y, ...) -> R' of TypedFunc
    Flexible case:
        > objects of 'tfunc_type_([X, Y, ...], cod=[R, S, ...])'
        > are objects 'f(*args)' of TypedFunc
        > whose argument type hints belong to 'coprod_(X, Y, ...)'
        > and whose return type hint belongs to 'coprod_(R, S, ...)'
    """
    if cod is None:
        raise TypeError("Codomain type must be specified.")

    flat_domain_types, domain_is_flexible = Helper.flat_(*domain_types)
    flat_codomain_types, codomain_is_flexible = Helper.flat_(cod)

    class _tfunc(TypedFunc):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, TypedFunc):
                return False

            domain_hints = hinted_domain(instance.func)
            return_type = hinted_codomain(instance.func)

            domain_check = (
                all(hint in flat_domain_types for hint in domain_hints)
                if domain_is_flexible else
                domain_hints == flat_domain_types
            )

            codomain_check = (
                return_type in flat_codomain_types
                if codomain_is_flexible else
                return_type == flat_codomain_types[0]
            )

            return domain_check and codomain_check

    class_name = (
        f"tfunc_({{{', '.join(t.__name__ for t in flat_domain_types)}}};"
        f" cod={{{', '.join(t.__name__ for t in flat_codomain_types)}}})"
    )
    return type(class_name, (_tfunc,), {})

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

    for f in funcs:
        if not callable(f):
            raise TypeError("Each function in 'funcs' must be callable.")

        domain_hints = hinted_domain(f)
        if any(hint != parent for hint in domain_hints):
            raise TypeError("Each function in 'funcs' must have a domain of 'prod_([parent])'.")

        if hinted_codomain(f) is not bool:
            raise TypeError(f"Each function in 'funcs' must be boolean: '{f.__name}' is not.")

    class _sub(parent):
        def __new__(cls, *args, **kwargs):
            instance = super(_sub, cls).__new__(cls, *args, **kwargs)
            if not all(f(instance, *args, **kwargs) for f in funcs):
                raise ValueError(f"Object does not satisfy all conditions in {funcs}.")
            return instance

    sub_class_name = f"sub_({parent.__name__})"
    return type(sub_class_name, (parent,), {})
