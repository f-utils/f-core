import inspect
from f import f
from f_core.mods.utils import flat_, func_instance_

class TypedFunc:
    def __init__(self, func):
        if not callable(func):
            raise TypeError(f"'{func}' is not a function.")
        self.func = func
        self._domain = self.calculate_domain()
        self._codomain = self.calculate_codomain()

    def calculate_domain(self):
        type_hints = get_type_hints(self.func)
        domain_hints = tuple(type_hints.values())[:-1]
        if domain_hints:
            return Builder.prod_type_(*domain_hints)
        return type(None)

    def calculate_codomain(self):
        type_hints = get_type_hints(self.func)
        return_hint = list(type_hints.values())[-1]
        if return_hint:
            return return_hint
        return type(None)

    @property
    def domain(self):
        return self._domain

    @property
    def codomain(self):
        return self._codomain

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __mul__(self, other):
        if not isinstance(other, TypedFunc):
            raise TypeError(f"'{other}' is not a valid typed function.")

        if not issubclass(other.codomain, self.domain):
            raise TypeError(f"Codomain '{other.codomain.__name__}' of '{other.func.__name__}' is not a subtype of the domain '{self.domain.__name__}' of '{self.func.__name__}'.")

        def composed(*args, **kwargs):
            return self.func(other.func(*args, **kwargs))

        return TypedFunc(composed)

class Builder:
    def coprod_type_(*types):
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

    def func_type_(*domain_types):
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

    def typed_func_type_(*domain_types, cod=None):
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
        class _sub(parent):
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

    # define 'tfunc' dspec
    f.ds.i(
        'tfunc_',
        'the typed function entity of entities',
        lambda *args, **kwargs: 'Typed function entity not defined for the variable types.'
    )

    f.ds.e(
        'tfunc_',
        f.t.E().keys(),
        Builder.typed_func_type_
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





