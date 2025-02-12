from f import f
from f_core.mods.op.prod_ import *
from f_core.mods.op.other_ import *
from f_core.mods.op.func_ import *


# define 'inter' type op
f.op.i(
    'inter_',
    'the intersection of types.',
    inter_type_
)

# define 'coprod' type op
f.op.i(
    'join_',
    'the join of types',
    join_type_
)

# define 'prod' type op
f.op.i(
    'prod_',
    'the product of types',
    prod_type_
)

# define 'unordered prod' type op
f.op.i(
    'unprod_',
    'the unordered product of types',
    unprod_type_
)

# define 'set prod' type op
f.op.i(
    'set_',
    'the set product of types',
    set_type_
)

# define 'dict prod' type op
f.op.i(
    'dict_',
    'the dict product of types',
    set_type_
)

# define 'hfunc' type op
f.op.i(
    'hfunc_',
    'the hinted function type of types',
    hfunc_type_
)

# define 'tfunc' type op
f.op.i(
    'tfunc_',
    'the typed function type of types',
    tfunc_type_
)

# define 'bfunc' type op
f.op.i(
    'bfunc_',
    'the boolean function type of types',
    bfunc_type_
)

# define 'sub' type op
f.op.i(
    'filter_',
    'build filtered subtype of types',
    filter_type_
)

# define 'compl' type op
f.op.i(
    'compl_',
    'the completion type by given subtype',
    compl_type_
)
