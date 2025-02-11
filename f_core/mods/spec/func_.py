from f import f
from f_core.mods.type.func_ import (
    PlainFunc,
    HintedFunc,
    TypedFunc,
    BooleanFunc
)

from f_core.mods.spec.helper_ import curry_

f.s.i(
    'curry_',
    'a general currying',
    lambda *args: f'The variables types are not valid for currying.'
)

f.s.e(
    'curry_',
    (TypedFunc, tuple),
    curry_
)
