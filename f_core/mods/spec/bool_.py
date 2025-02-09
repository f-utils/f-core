from f import f
from f_core.mods.type.main_ import *
from f_core.mods.glob_ import Is as is_
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


# add 'less_than' spectra

f.s.i(
    'less_than_',
    'Check if something is less than something else',
    lambda *args, **kwargs: 'The provided types are not acceptable for the less than operation.'
)


f.s.i(
    'less_than_',
    'Check if something is less than something else',
    lambda *args, **kwargs: 'The provided types are not acceptable for the less than operation.'
)

f.s.e(
    'less_than_',
    (type, type),
    lambda x,y: issubclass(x, y)
)

for t in (t in Any.tuple(t) if is_.seq(t)):
    f.s.e(
        'less_than_',
        (, type),
        lambda x,y: issubclass(x, y)
    )


# add 'has_' spectra

f.s.i(
    'has_',
    'Check if something has something else'
)


