from f import f
from f_core.mods.type.main_ import StrucTypes as struc
from f_core.mods.spec.helper_ import (
    inter_tuple,
    inter_list,
    inter_set,
    inter_dict,
    inter_str
)

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
