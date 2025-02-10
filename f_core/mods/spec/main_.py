from f_core.mods.spec.type_ import *
from f_core.mods.spec.bool_ import *
from f_core.mods.spec.func_ import *

class Specs:
    attr    = f.s('attr_')
    inter   = f.ds('inter_')
    prod    = f.ds('prod_')
    coprod  = f.ds('coprod_')
    compl   = f.s('compl_')
    belongs = f.s('belongs_')
    bl      = belongs
