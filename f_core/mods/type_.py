from f import f
import inspect
from typing import get_type_hints


class TypedFunc:
    def __init__(self, func):
        if not callable(func):
            raise TypeError(f"'{func}' is not a function.")
        self.func = func
        self.signature = inspect.signature(func)
        self._domain = self.calculate_domain()
        self._codomain = self.calculate_codomain()

    def calculate_domain(self):
        param_types = [
            param.annotation if param.annotation != inspect.Parameter.empty else type(None)
            for param in self.signature.parameters.values()
        ]
        print(f"Param types for {self.func.__name__}: {param_types}")  # Debugging line
        return Builder.prod_type_(*param_types) 

    def calculate_codomain(self):
        return_annotation = inspect.signature(self.func).return_annotation
        return return_annotation if return_annotation != inspect.Signature.empty else type(None) 

    @property
    def domain(self):
        return self._domain

    @property
    def codomain(self):
        return self._codomain

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __mul__(self, other):
        if not isinstance(other, Types.typed_func):
            raise TypeError(f"'{other}' is not a valid typed function.")

        if not issubclass(other.codomain, self.domain):
            raise TypeError(f"Codomain '{self.codomain.__name__}' of '{self.func.__name__}' is not a subtype of the domain '{other.domain.__name__}' of '{other.func.__name__}'.")

        def composed(*args, **kwargs):
            return other(self.func(*args, **kwargs))

        return Types.typed_func(composed)

class Builder:
    def coprod_type_(*types):
        if len(types) == 0:
            return type(None)
        elif len(types) == 1:
            return types[0]

        for typ in types:
            if not isinstance(typ, type):
                raise TypeError(f"{typ} is not a valid type.")

        class _coprod(type):
            def __instancecheck__(cls, instance):
                return any(isinstance(instance, typ) for typ in cls._types)

        class coprod_(metaclass=_coprod):
            _types = types
        return coprod_

    def prod_type_(*types):
        if len(types) == 0:
            return type(None)
        elif len(types) == 1:
            return types[0]

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

        class_name = f"prod_({', '.join(t.__name__ for t in types)})"
        prod_ = _prod(class_name, (), {"_types": types})
        return prod_

    def unprod_type_(*types):
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

    def func_type_(*expected_types):
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
                    raise ValueError(f"Condition {f} not satisfied for this instance.")
        return _sub

class Specs:
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
        Builder.coprod_type_
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
        Builder.prod_type_
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
        Builder.unprod_type_
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
        Builder.func_type_
    )

    # # define sub dspec
    # f.s.i(
    #     'sub_',
    #     'build a subobject from a given object',
    #     lambda *args, **kwargs: 'Subobject not defined for the variable types.'
    # )

    # f.s.e(
    #     'sub_',
    #     type,
    # )





