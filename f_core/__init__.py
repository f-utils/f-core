from f_core.mods.type_ import TypedFunc
from f_core.mods.type_ import Specs
from f_core.mods.func_ import *
from f_core.mods.mon_  import *
from f_core.mods.spec_ import *
from f_core.mods.var_  import *

# set primitive types
class Types:
    tfunc = TypedFunc
    tf = tfunc
t = Types

# set primitive specs
prod_   = f.ds('prod_')
coprod_ = f.ds('coprod_')
unprod_ = f.ds('unprod_')
func_   = f.ds('func_')
