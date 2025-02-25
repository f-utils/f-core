from f_core.mods.type.helper_ import flat_, prod_

def join_type_(*types):
    """
    Build the 'join' of types:
        > an object 'p' of the join between 'X, Y, ...'
        > is an object of some of 'X, Y, ...'
    """
    flat_types, is_flexible = flat_(*types)

    class _join(type):
        def __instancecheck__(cls, instance):
            return isinstance(instance, tuple(flat_types))

        def check(self, instance):
            return isinstance(instance, tuple(self.__types__))

    class_name = f"join_({', '.join(t.__name__ for t in flat_types)})"
    return _join(class_name, (), {'__types__': flat_types})

def prod_type_(*types):
    """
    Build the 'product' of types:
        > the objects of the product between 'X, Y, ...'
        > are the tuples '(x, y, ...)' such that
        > 'x, y, ...' are in 'X, Y, ...'
    """
    flat_types, is_flexible = flat_(*types)

    class _prod(type):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, tuple):
                return False
            if len(instance) != len(flat_types):
                return False
            return all(isinstance(x, t) for x, t in zip(instance, flat_types))

        def check(self, instance):
            if not isinstance(instance, tuple):
                return False
            if len(instance) != len(self.__types__):
                return False
            return all(isinstance(x, t) for x, t in zip(instance, self.__types__))

    class_name = f"prod_({', '.join(t.__name__ for t in flat_types)})"
    return _prod(class_name, (tuple,), {'__types__': flat_types})

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

        def check(self, instance):
            if not isinstance(instance, set):
                return False
            return all(any(isinstance(elem, typ) for typ in self.__types__) for elem in instance)


    if is_flexible:
        class_name = f"unprod_[{', '.join(t.__name__ for t in flat_types)}]"
    else:
        class_name = f"unprod_({', '.join(t.__name__ for t in flat_types)})"
    return _unprod(class_name, (set,), {'__types__': flat_types})
