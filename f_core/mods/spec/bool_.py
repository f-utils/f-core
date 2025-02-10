from f import f
from f_core.mods.type.main_ import BooleanFunc, Any
from f_core.mods.glob.is_ import Is as is_
from f_core.mods.spec.helper_ import *

# add 'belongs' spectra
f.s.i(
    'belongs_',
    'Check if something belongs to something else',
    lambda *args, **kwargs: 'The provided types are not acceptable for the belonging operation.'
)

f.s.e(
    'belongs_',
    ('Any', [t for t in Any.tuple() if is_.cont(t)]),
    lambda x,y: x in y
)

f.s.e(
    'belongs_',
    ([t for t in Any.tuple() if t is not type], type),
    lambda x,y: isinstance(x, y)
)

# add 'not' spectra
f.s.i(
    'not_',
    'Negate something.',
    lambda *args, **kwargs: 'The provided types cannot be negated.'
)

f.s.e(
    'not_',
    (bool, ),
    lambda x: not x
)

f.s.e(
    'not_',
    (BooleanFunc, ),
    n_
)
