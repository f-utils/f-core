from f import f
import inspect
from typing import get_type_hints

# the class with bare types
class Types:
    class func:
        def __init__(self, func):
            if not callable(func):
                raise funcErr(f"'{func}' is not a function.")
            self._func = func

        def __call__(self, *args, **kwargs):
            return self._func(*args, **kwargs)

        def __mul__(self, other):
            if not isinstance(other, f.func):
                raise funcErr(f"'{other}'is not a function: the composition is defined only between functions.")
            def comp_(*args, **kwargs):
                return self._func(other(*args, **kwargs))
            return f.func(comp_)

    class typed_func:
        def __init__(self, func: Callable):
            if not callable(func):
                raise funcErr(f"{func} is not a function.")
            self.func = func
            self.annotations = self._get_type_hints(func)

        def _get_type_hints(self, obj) -> Dict[str, Any]:
            return inspect.getfullargspec(obj).annotations

        @property
        def domain(self):
            param_types = {k: v for k, v in self.annotations.items() if k != 'return'}
            return self._create_domain_class(param_types)

        def _create_domain_class(self, param_types) -> type:
            class _domain:
                def __init__(self, *args):
                    if len(args) != len(param_types):
                        raise TypeError("Number of arguments must match the parameter types.")
                    for arg, (param, expected_type) in zip(args, param_types.items()):
                        if not isinstance(arg, expected_type):
                            raise TypeError(f"Argument {param} must be of type {expected_type.__name__}.")

                @classmethod
                def validate(cls, value_type: type) -> bool:
                    return issubclass(value_type, list(param_types.values())[0]) if param_types else False

                def __repr__(self):
                    return f"_domain({', '.join(f'{param}: {expected_type.__name__}' for param, expected_type in param_types.items())})"
            return _domain

        @property
        def codomain(self) -> Any:
            return self.annotations.get('return', None)

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        def __mul__(self, other: Callable):
            if not isinstance(other, Callable):
                raise funcErr(f"'{other}' is not a function.")
            other_func = typed_func(other)
            if not self.domain.validate(other_func.codomain):
                raise funcErr(f"Codomain '{self.func.codomain}' of '{self.func}' is not a subtype of the domain '{other_func.domain}' of '{other_func}'.")
            def comp_(*args, **kwargs):
                return self.func(other(*args, **kwargs))
            return typed_func(comp_)
t = Types

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

# define 'attr' spec
f.s.i(
    'attr_',
    'attribute something to a given entity',
    lambda *args, **kwargs: 'The variable types cannot be attributed to some entity.'
)

f.s.e(
    'attr_',
    (type, str, type),
    lambda x, y, z: setattr(x, y, z)
)

# define 'coprod' dspec
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

# define 'prod' dspec
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

# define 'unordered prod' dspec
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

# define 'func' dspec
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





