from f import f
from f_core.mods.type.main_ import *
from f_core.mods.spec.type_ import *
from f_core.mods.spec.bool_ import *
from f_core.mods.spec.func_ import *
from f_core.mods.spec.var_  import *

# set main types
class Types(FuncTypes):
    Any = Any
    pass

# set main specs
class Specs:
    attr_    = f.s('attr_')
    prod_    = f.ds('prod_')
    coprod_  = f.ds('coprod_')
    unprod_  = f.ds('unprod_')
    rdfunc_  = f.ds('rdfunc_')
    rcfunc_  = f.ds('rcfunc_')
    rfunc_   = f.ds('rfunc_')
    hdfunc_  = f.ds('hdfunc_')
    hcfunc_  = f.ds('hcfunc_')
    hfunc_   = f.ds('hfunc_')
    tdfunc_  = f.ds('tdfunc_')
    tcfunc_  = f.ds('tcfunc_')
    tfunc_   = f.ds('tfunc_')
    bfunc_   = f.ds('bfunc_')
    sub_     = f.s('sub_')
    compl_   = f.s('compl_')
    belongs_ = f.s('belongs_')
    bl_      = belongs_
    not_     = f.s('not_')
