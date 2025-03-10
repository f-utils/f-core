from f import f
from f_core.mods.op.prod_ import (
    join_type_,
    prod_type_
)
from f_core.mods.op.other_ import (
    inter_type_,
    filter_type_,
    compl_type_
)
from f_core.mods.type.main_ import BooleanFunc


# define 'inter' dspec
f.ds.i(
    'inter_',
    'the intersection of entities',
    lambda *args, **kwargs: 'Intersection not defined for the variable types.'
)

f.ds.e(
    'inter_',
    [type],
    inter_type_
)

# define 'coprod' dspec
f.ds.i(
    'join_',
    'the join of entities',
    lambda *args, **kwargs: 'Join not defined for the variable types.'
)

f.ds.e(
    'join_',
    [type],
    join_type_
)

# define 'prod' dspec
f.ds.i(
    'prod_',
    'the product of entities',
    lambda *args, **kwargs: 'Product not defined for the variable types.'
)

f.ds.e(
    'prod_',
    [type],
    prod_type_
)

# define 'sub' spec
f.s.i(
    'filter_',
    'the filtered subentity of entities',
    lambda *args, **kwargs: 'Filtering not defined for the variable types.'
)

f.s.e(
    'filter_',
    (type, BooleanFunc),
    filter_type_
)

# define 'compl' dspec
f.s.i(
    'compl_',
    'the completion entity by given subentities',
    lambda *args, **kwargs: 'Completion not defined for the variable types.'
)

f.s.e(
    'compl_',
    (type, type),
    compl_type_
)
