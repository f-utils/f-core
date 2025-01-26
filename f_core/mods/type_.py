from f import f
import inspect
from typing import get_type_hints

class Builder:
    def type_coprod_(*types):
        for typ in types:
            if not isinstance(typ, type):
                raise TypeError(f"{typ} is not a valid type.")

        class _coprod(type):
            def __instancecheck__(cls, instance):
                return any(isinstance(instance, typ) for typ in cls._types)

        class coprod_(metaclass=_coprod):
            _types = types
        return coprod_

    def type_prod_(*types):
        for typ in types:
            if not isinstance(typ, type):
                raise TypeError(f"{typ} is not a valid type.")

        class _prod(type):
            def __instancecheck__(cls, instance):
                if not isinstance(instance, tuple):
                    return False
                if len(instance) != len(cls._types):
                    return False
                return all(isinstance(elem, typ) for elem, typ in zip(instance, cls._types))

        class prod_(metaclass=_prod):
            _types = types
        return prod_

    def type_unprod_(*types):
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

    def type_func_(*expected_types):
        class _func(type):
            def __instancecheck__(cls, instance):
                if not callable(instance):
                    return False

                type_hints = get_type_hints(instance)
                param_hints = list(type_hints.values())[:-1]

                return param_hints == list(expected_types)

        class func_(metaclass=_func):
            _types = expected_types
        return func_

    def type_sub_(X, f):
        class _sub(X):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not f(self):
                raise ValueError(f"Condition not satisfied for this instance.")
    return _sub

# define coprod dspec
f.ds.i(
    'coprod_',
    'the coproduct of entities',
    lambda *args, **kwargs: 'Coproduct not defined for the variable types.'
)

f.ds.e(
    'coprod_',
    f.t.E().keys(),
    Builder.type_coprod_
)

# define prod dspec
f.ds.i(
    'prod_',
    'the product of entities',
    lambda *args, **kwargs: 'Product not defined for the variable types.'
)

f.ds.e(
    'prod_',
    f.t.E().keys(),
    Builder.type_prod_
)

# define unordered prod dspec
f.ds.i(
    'unprod_',
    'the unordered product of entities',
    lambda *args, **kwargs: 'Unordered product not defined for the variable types.'
)

f.ds.e(
    'unprod_',
    f.t.E().keys(),
    Builder.type_unprod_
)

# define func dspec
f.ds.i(
    'func_',
    'the function entity of entities',
    lambda *args, **kwargs: 'Function entity not defined for the variable types.'
)

f.ds.e(
    'func_',
    f.t.E().keys(),
    Builder.type_func_
)

# define sub dspec
f.s.i(
    'sub_',
    'build a subobject from a given object',
    lambda *args, **kwargs: 'Subobject not defined for the variable types.'
)

f.s.e(
    'sub_',
    type,
)





