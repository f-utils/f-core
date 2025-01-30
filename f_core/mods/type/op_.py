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
    flat_types = flat_(*types)[0]
    is_flexible = flat_(*types)[1]

    if len(flat_types) == 0:
        return type(None)
    elif len(flat_types) == 1 and not is_flexible:
        return flat_types[0]

    class _prod(type):
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

    if is_flexible:
        class_name = f"prod_[{', '.join(t.__name__ for t in flat_types)}]"
    else:
        class_name = f"prod_({', '.join(t.__name__ for t in flat_types)})"
    prod_ = _prod(class_name, (), {})

    return prod_

# TODO: add  flexible case for unprod
def unprod_type_(*types):
    """
    Build the 'unordered product' of types:
        > the objects of the unproduct between 'X, Y, ...'
        > are the sets '{x, y, ...}' such that
        > 'x, y, ...' are in 'X, Y, ...'
    """
    if len(types) == 0:
        return None
    elif len(types) == 1:
        return types[0]

    for typ in types:
        if not isinstance(typ, type):
            raise TypeError(f"{typ} is not a valid type.")

    class _unprod(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, set):
                return False
            type_counts = {typ: types.count(typ) for typ in types}
            for elem in instance:
                for typ in type_counts:
                    if isinstance(elem, typ) and type_counts[typ] > 0:
                        type_counts[typ] -= 1
                        break
                else:
                    return False
            return all(count == 0 for count in type_counts.values())

    class unprod_(metaclass=_unprod):
        _types = types
    return unprod_

# TODO 
def setprod_type_(*types):
    """
    Build the 'set product' of types:
        > the objects of the set product between 'X, Y, ...'
        > are the sets '{x, y, ...}' such that
        > 'x, y, ...' are in the coproduct between 'X, Y, ...'
    """
    pass

# TODO
def dicprod_type_(*types):
    """
    Build the 'dictionary product' of types:
        > the objects of the dicproduct between '{X0: X1, Y0: Y1, ...}'
        > are the dictionaries '{x0: x1, y0: y1, ...}' such that
        > 'x0, y0, ...' are in 'X0, Y0, ...'
        > 'x1, y1, ...' are in 'X1, Y1, ...'
    """
    pass


# TODO
def hfunc_type_(*domain_types, cod=None):
    """
    Build the 'hinted function type' of types:
        > the objects of the function type between X, Y, ...
        > are objects 'f(x: X, y: Y, ...) -> R' of HintedFunc such that
        > 'x, y, ...' are hinted to 'X, Y, ...'
    """
    pass

# TODO: refactor this to use the RuntimedFunc class
def rfunc_type_(*domain_types):
    """
    Build the 'runtimed function type' of types:
        > the objects of the function type between X, Y, ...
        > are objects 'f(x, y, ...)' of RuntimedFunc such that
        > 'x, y, ...' are in 'X, Y, ...' at runtime
    """
    if not domain_types:
        raise TypeError("Domain types cannot be empty.")
    for typ in domain_types:
        if not isinstance(typ, type) and not isinstance(type, list):
            raise TypeError(f"{typ} is not a valid type.")
    is_flexible = False
    flat_types = []

    if len(domain_types) == 1 and isinstance(domain_types[0], list):
        is_flexible = True
        flat_types = tuple(domain_types[0])
    else:
        flat_types = domain_types

    class _func(type):
        def __instancecheck__(cls, instance):
            if isinstance(instance, TypedFunc):
                instance = instance.func
            else:
                try:
                    instance = TypedFunc(instance).func
                except Exception as e:
                    AttributeError("Could not turn '{isinstance}' into a typed function: {e}")

            if not callable(instance):
                return False

            type_hints = get_type_hints(instance)
            param_hints = tuple(type_hints.values())[:-1]

            if is_flexible:
                for x in param_hints:
                    if not x in flat_types:
                        return False
                return True
            return param_hints == flat_types

    class func_(metaclass=_func):
        _types = flat_types

    return func_

# TODO: refactor this to produce a subtype of hfunc_type
def tfunc_type_(*domain_types, cod=None):
    """
    Build the 'typed function type' of types:
        > the objects of the typed function type between X, Y, ..., R
        > are objects of TypedFunc such that f(x: X, y: Y, ...) -> R
    """
    if not domain_types:
        raise TypeError("Domain types cannot be empty.")
    for typ in domain_types:
        if not isinstance(typ, type) and not isinstance(typ, list):
            raise TypeError(f"{typ} is not a valid type.")
    if cod:
        if not isinstance(cod, type):
            raise TypeError(f"{cod} must be a type type.")
    else:
        raise AttributeError("Argument 'cod' must be provided.")

    if len(domain_types) == 1 and isinstance(domain_types[0], list):
        flat_types = tuple(domain_types[0])
        is_flexible = True
    else:
        flat_types = domain_types
        is_flexible = False

    class _typed_func(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, TypedFunc):
                try:
                    instance = TypedFunc(instance)
                except:
                    return False
            if not callable(instance):
                return False

            type_hints = get_type_hints(instance.func)
            domain_hints = tuple(type_hints.values())[:-1]
            return_hint = tuple(type_hints.values())[-1]
            if not return_hint == cod:
                return False

            if is_flexible:
                for x in domain_hints:
                    if not x in flat_types:
                        return False
                return True
            return domain_hints == flat_types

    if is_flexible:
        domain_type_names = "["+", ".join(t.__name__ for t in flat_types)+"]"
    domain_type_names = ", ".join(t.__name__ for t in flat_types)
    class_name = f"tfunc_({{{domain_type_names}}}; {cod.__name__})"

    return _typed_func(class_name, (), {})

def sub_type_(parent, f):
    if not isinstance(parent, type):
        raise TypeError(f"Variable '{parent}' is not a type.")
    class _sub(parent):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not f(self):
                raise ValueError(f"Condition '{f}' not satisfied for this instance.")
    return _sub
