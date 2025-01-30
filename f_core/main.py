from f_core.mods.type_ import TypedFunc
from f_core.mods.type_ import Specs

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
tfunc_  = f.ds('tfunc_')
