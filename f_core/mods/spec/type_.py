from f import f
from f_core.mods.type.op_ import *

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

# # define 'func' dspec
# f.ds.i(
#     'func_',
#     'the function entity of entities',
#     lambda *args, **kwargs: 'Function entity not defined for the variable types.'
# )

# f.ds.e(
#     'func_',
#     f.t.E().keys(),
#     func_type_
# )

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

# define sub dspec
f.s.i(
    'sub_',
    'build a subobject from a given object',
    lambda *args, **kwargs: 'Subobject not defined for the variable types.'
)
