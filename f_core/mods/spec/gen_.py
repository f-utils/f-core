from f import f
from f_core.mods.spec.helper_ import (
    append_list,
    append_set,
    append_general
)
from f_core.mods.type.main_ import StrucTypes as struc

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

