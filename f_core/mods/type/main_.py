from f import f
from f_core.mods.type.type_ import *
from f_core.mods.type.op_ import (
    coprod_type_
)

# set the primitive func types
class FuncTypes:
    PlainFunc     = PlainFunc
    HintedDomFunc = HintedDomFunc
    HintedCodFunc = HintedCodFunc
    HintedFunc    = HintedFunc
    TypedDomFunc  = TypedDomFunc
    TypedCodFunc  = TypedCodFunc
    TypedFunc     = TypedFunc
    BooleanFunc   = BooleanFunc
    PF            = PlainFunc
    HDF           = HintedDomFunc
    HCF           = HintedCodFunc
    HF            = HintedFunc
    TDF           = TypedDomFunc
    TCF           = TypedCodFunc
    TF            = TypedFunc
    BF            = BooleanFunc

class Any:
    _initial_any = coprod_type_(*f.t.E().keys())
    @staticmethod
    def get():
        return coprod_type_(*f.t.E().keys())

# include the primitive func types
f.t.i(
    FuncTypes.PF,
    'Plain functions: compasable and callable objects'
)

f.t.i(
    FuncTypes.HF,
    'Hinted functions: compasable and callable objects with defined type hints'
)

f.t.i(
    FuncTypes.TF,
    'Typed functions: compasable and callable objects with defined type hints and runtime type checking'
)

f.t.i(
    FuncTypes.BF,
    'Typed functions: compasable and callable objects with defined type hints and runtime type checking'
)

# include the dynamic 'Any' type
f.t.i(
    Any,
    'The type of anything.'
)


