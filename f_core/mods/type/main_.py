from f import f
from f_core.mods.type.func_  import *
from f_core.mods.type.struc_ import *
from f_core.mods.op.prod_    import join_type_
from collections.abc import (
    Sequence,
    Sized,
    Container,
    Iterable,
    Hashable,
    Mapping,
    Callable
)

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

class StrucTypes:
    Callable   = Callable
    Sequence   = Sequence
    Sized      = Sized
    Container  = Container
    Iterable   = Iterable
    Hashable   = Hashable
    Nullable   = Nullable
    Appendable = Appendable
    Mapping    = Mapping
    Call       = Callable
    Seq        = Sequence
    Szd        = Sized
    Cont       = Container
    Cnt        = Cont
    Iter       = Iterable
    Hash       = Hashable
    Append     = Appendable
    App        = Append
    Map        = Mapping
    Null       = Nullable

class Any:
    _initial_any = join_type_(*f.t.E().keys())
    @staticmethod
    def get():
        return join_type_(*f.t.E().keys())
    def tuple():
        return f.t.E().keys()

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

# include the primitive structural types
f.t.i(
    StrucTypes.Call,
    'Callable: has method __call__'
)
f.t.i(
    StrucTypes.Cont,
    'Containers: has method __contains__'
)
f.t.i(
    StrucTypes.Hash,
    'Hashable classes: has method __hash__'
)
f.t.i(
    StrucTypes.Sized,
    'Sized classes: has method __len__'
)
f.t.i(
    StrucTypes.Iter,
    'Iterable classes: has method __iter__'
)
f.t.i(
    StrucTypes.Seq,
    'Sequence classes: sized and has method __getitem__'
)
f.t.i(
    StrucTypes.Map,
    'Sequence classes: iterable, sized and has method __getitem__'
)
f.t.i(
    StrucTypes.Null,
    'Nullable classes: has the method __null__'
)
f.t.i(
    StrucTypes.Append,
    'Appendable classes: container with method __append__'
)

# include the dynamic 'Any' type
f.t.i(
    Any,
    'The type of anything.'
)
