from f import f
from f_core.mods.type.main_ import *
from f_core.mods.spec.type_ import *
from f_core.mods.spec.bool_ import *
from f_core.mods.spec.func_ import *
from f_core.mods.glob_      import *

# set main types
class Types(FuncTypes):
    Any = Any
    pass

# set main specs
class Specs:
    attr    = f.s('attr_')
    inter   = f.ds('inter_')
    prod    = f.ds('prod_')
    coprod  = f.ds('coprod_')
    unprod  = f.ds('unprod_')
    rdfunc  = f.ds('rdfunc_')
    rcfunc  = f.ds('rcfunc_')
    rfunc   = f.ds('rfunc_')
    hdfunc  = f.ds('hdfunc_')
    hcfunc  = f.ds('hcfunc_')
    hfunc   = f.ds('hfunc_')
    tdfunc  = f.ds('tdfunc_')
    tcfunc  = f.ds('tcfunc_')
    tfunc   = f.ds('tfunc_')
    bfunc   = f.ds('bfunc_')
    sub     = f.s('sub_')
    compl   = f.s('compl_')
    belongs = f.s('belongs_')
    bl      = belongs

class Globals:
    is_ = Is
    i = is_
