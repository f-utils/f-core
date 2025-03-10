from f_core.mods.spec.type_ import *
from f_core.mods.spec.bool_ import *
from f_core.mods.spec.func_ import *
from f_core.mods.spec.gen_ import *

class Specs:
    inter   = f.ds('inter_')
    prod    = f.ds('prod_')
    join    = f.ds('join_')
    filter  = f.s('filter_')
    compl   = f.s('compl_')
    belongs = f.s('belongs_')
    bl      = belongs
    n       = f.s('not_')
    curry   = f.s('curry_')
    append  = f.s('append_')
