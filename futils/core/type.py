from futils import *
from logs import *
from op import *
from typing import NamedTuple

def typename(t):
    return t().__class__.__name__

def prod(*types):
    for t in types:
        if nb(t, type):
            err("Arguments must be types.")
    fields = {f"t{i}": t for i, t in enum(types)}
    return NamedTuple("ProductType", fields)

def coprod(*types):
    for t in types:
        if nb(t, type):
            err("Arguments must be types.")
    class Coproduct:
        def __new__(cls, value):
            if nb(value, cls.valid_types):
                err(f"Value must be one of the types: {[t.__name__ for t in cls.valid_types]}")
            return value
        @classmethod
        def __instancecheck__(cls, instance):
            return bl(instance, cls.valid_types)
    Coproduct.valid_types = tuple(types)
    return Coproduct

