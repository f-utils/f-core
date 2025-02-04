from f import f
from f_core.mods.type.type_ import *
from f_core.mods.spec.type_ import *

# set primitive types
class Types:
    pfunc = PlainFunc
    hdfunc = HintedDomFunc
    hcfunc = HintedCodFunc
    hfunc = HintedFunc
    tdfunc = TypedDomFunc
    tcfunc = TypedCodFunc
    tfunc = TypedFunc
    bfunc = BooleanFunc

# set primitive modads
class Monads:
    pass

# set primitive specs
class Specs:
    prod_   = f.ds('prod_')
    coprod_ = f.ds('coprod_')
    unprod_ = f.ds('unprod_')
    rdfunc_ = f.ds('rdfunc_')
    rcfunc_ = f.ds('rcfunc_')
    rfunc_  = f.ds('rfunc_')
    hdfunc_ = f.ds('hdfunc_')
    hcfunc_ = f.ds('hcfunc_')
    hfunc_  = f.ds('hfunc_')
    tdfunc_ = f.ds('tdfunc_')
    tcfunc_ = f.ds('tcfunc_')
    tfunc_  = f.ds('tfunc_')
    bfunc_  = f.ds('bfunc_')
    sub_    = f.s('sub_')
    compl_  = f.s('compl_')