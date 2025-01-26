from f import f

class Utils:
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

f.ds.i(
    'coprod_',
    'the coproduct of entities',
    lambda *args, **kwargs: 'Coproduct not defined for the variable types.'
)

f.ds.e(
    'coprod_',
    f.t.E().keys(),
    Utils.type_coprod_
)

f.ds.i(
    'prod_',
    'the product of entities',
    lambda *args, **kwargs: 'Product not defined for the variable types.'
)

f.ds.e(
    'prod_',
    f.t.E().keys(),
    Utils.type_prod_
)

