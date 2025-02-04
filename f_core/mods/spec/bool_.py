from f import f
from f_core.mods.type.main_ import *
from f_core.mods.spec.helper_ import *

# add 'belongs' spectra
f.s.i(
    'belongs_',
    'Check if something belongs to something else.',
    lambda *args, **kwargs: 'The provided types are not acceptable for the belonging operation.'
)

f.s.e(
    'belongs_',
    (type, type),
    subclass_
)

f.s.e(
    'belongs_',
    (Any, type),
    instance_
)


