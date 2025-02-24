from f import f
from f_core.mods.type.main_ import *
from f_core.mods.op.main_   import *
from f_core.mods.spec.main_ import *
from f_core.mods.glob.main_ import *


class Types(FuncTypes):
    Any   = Any
    any   = Any

class Globals:
    Is = Is
    is_ = Is
    i = is_
    Sub = Sub
    sub = Sub
    s = sub

class Ops(Ops):
    pass

class Specs(Specs):
    pass

typed = typed
