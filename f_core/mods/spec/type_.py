from f import f
from f_core.mods.type.op_ import *
from f_core.mods.type.type_ import (
    PlainFunc,
    HintedFunc,
    TypedFunc,
    BooleanFunc
)

# turn basic func type classes as accessible types
f.t.i(
    PlainFunc,
    'The class of composable callable objects.'
)
f.t.i(
    HintedFunc,
    'The class of composable callable objects with type hints.'
)
f.t.i(
    TypedFunc,
    'The class of composable callable objects with type hints checked at runtimes.'
)
f.t.i(
    BooleanFunc,
    'The class of boolean typed functions.'
)

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
    coprod_type_
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
    prod_type_
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
    unprod_type_
)

# define 'set prod' dspec
f.ds.i(
    'set_',
    'the set product of entities',
    lambda *args, **kwargs: 'Set product not defined for the variable types.'
)

f.ds.e(
    'set_',
    f.t.E().keys(),
    set_type_
)

# define 'dict prod' dspec
f.ds.i(
    'dict_',
    'the dict product of entities',
    lambda *args, **kwargs: 'Dict product not defined for the variable types.'
)

f.ds.e(
    'dict_',
    f.t.E().keys(),
    set_type_
)


# define 'hfunc' dspec
f.ds.i(
    'hfunc_',
    'the hinted function entity of entities',
    lambda *args, **kwargs: 'Hinted function entity not defined for the variable types.'
)

f.ds.e(
    'hfunc_',
    f.t.E().keys(),
    hfunc_type_
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
    tfunc_type_
)

# define 'bfunc' dspec
f.ds.i(
    'bfunc_',
    'the boolean function entity of entities',
    lambda *args, **kwargs: 'Boolean function entity not defined for the variable types.'
)

f.ds.e(
    'bfunc_',
    f.t.E().keys(),
    bfunc_type_
)

# define 'sub' spec
f.s.i(
    'sub_',
    'the subentity of entities',
    lambda *args, **kwargs: 'Subentity not defined for the variable types.'
)

f.s.e(
    'sub_',
    (type, BooleanFunc),
    sub_type_
)


