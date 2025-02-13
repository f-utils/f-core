from f import f
from f_core.mods.type.main_ import StrucTypes as struc
from f_core.mods.type.func_ import BooleanFunc
from f_core.mods.spec.helper_ import *

# define 'append' spec
f.s.i(
    'append_',
    'Append something to something else.',
    lambda *args: 'The variable types does not support appending.'
)

f.s.e(
    'append_',
    ('Any', list),
    lambda x, y: y.append(x)
)

f.s.e(
    'append_',
    ('Any', set),
    lambda x, y: y.add(x)
)

f.s.e(
    'append_',
    (dict, dict),
    lambda x, y: y.update(x)
)

f.s.e(
    'append_',
    ('Any', struc.App),
    lambda x, y: y.__append__(x)
)

# extend the 'inter' dspec
f.ds.e(
    'inter_',
    [str],
    inter_str
)

f.ds.e(
    'inter_',
    [tuple],
    inter_tuple
)

f.ds.e(
    'inter_',
    [list],
    inter_list
)

f.ds.e(
    'inter_',
    [set],
    inter_set
)

f.ds.e(
    'inter_',
    [frozenset],
    lambda *frozensets: frozenset.intersection(*frozensets)
)

f.ds.e(
    'inter_',
    [dict],
    inter_dict
)

# extend 'join' dspec
f.ds.e(
    'join_',
    [str],
    join_str
)

f.ds.e(
    'join_',
    [tuple],
    join_tuple
)

f.ds.e(
    'join_',
    [list],
    join_list
)

f.ds.e(
    'join_',
    [set],
    join_set
)

f.ds.e(
    'join_',
    [dict],
    join_dict
)

# extend the 'filter' dspec
f.s.e(
    'filter_',
    (str, BooleanFunc),
    filter_str
)

f.s.e(
    'filter_',
    (tuple, BooleanFunc),
    filter_tuple
)

f.s.e(
    'filter_',
    (list, BooleanFunc),
    filter_list
)

f.s.e(
    'filter_',
    (set, BooleanFunc),
    filter_set
)

f.s.e(
    'filter_',
    (dict, BooleanFunc),
    filter_dict
)

# extend the 'compl' dspec
f.s.e(
    'compl_',
    (str, str),
    compl_str
)

f.s.e(
    'compl_',
    (tuple, tuple),
    compl_tuple
)

f.s.e(
    'compl_',
    (list, list),
    compl_list
)

f.s.e(
    'compl_',
    (set, set),
    compl_set
)

f.s.e(
    'compl_',
    (dict, dict),
    compl_dict
)

# extend the 'prod' dspec
f.ds.e(
    'prod_',
    [str],
    prod_str
)

f.ds.e(
    'prod_',
    [tuple],
    prod_tuple
)

f.ds.e(
    'prod_',
    [list],
    prod_list
)

f.ds.e(
    'prod_',
    [set],
    prod_set
)

f.ds.e(
    'prod_',
    [dict],
    prod_dict
)
