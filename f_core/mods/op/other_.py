from f_core.mods.type.helper_ import flat_

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


def tuple_type_(*args):
    """
    Define a metaclass for tuples that consist of specified types.
    This function accepts either:
      - Unpacked types (e.g., tuple_type_(type1, type2, ...))
      - A single list of types (e.g., tuple_type_([type1, type2, ...]))
    """
    flat_types, is_flexible = flat_(*args)

    # Ensure all elements are types
    if not all(isinstance(t, type) for t in flat_types):
        raise TypeError("All elements must be types.")

    class TupleMeta(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, tuple):
                return False
            if len(instance) != len(flat_types):
                return False
            return all(isinstance(x, t) for x, t in zip(instance, flat_types))

    class_name = f"tuple_({', '.join(t.__name__ for t in flat_types)})"
    return TupleMeta(class_name, (tuple,), {'__types__': flat_types})

def list_type_(*args):
    """
    Define a metaclass for lists that consist of specified types.
    This function accepts either:
      - Unpacked types (e.g., list_type_(type1, type2, ...))
      - A single list of types (e.g., list_type_([type1, type2, ...]))
    """
    flat_types, is_flexible = flat_(*args)

    if not all(isinstance(t, type) for t in flat_types):
        raise TypeError("All elements must be types.")

    class ListMeta(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, list):
                return False
            return all(any(isinstance(x, t) for t in flat_types) for x in instance)

    class_name = f"list_([{', '.join(t.__name__ for t in flat_types)}])"

    return ListMeta(class_name, (list,), {'__types__': flat_types})

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

def filter_type_(parent, *funcs):
    """
    Build the subtype 'filter_type(X, *funcs)' of a 'parent' type such that:
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

    class _filter(parent):
        def __init__(self, value):
            if not all(func.func(value) for func in funcs):
                raise ValueError("Object does not satisfy all conditions in the given funcs.")
            super().__init__()

        def __instancecheck__(cls, instance):
            return isinstance(instance, parent) and all(func.func(instance) for func in funcs)

    sub_class_name = f"filter_({parent.__name__})"
    return type(sub_class_name, (_filter,), {})

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
