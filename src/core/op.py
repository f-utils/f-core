import sys, os
sys.path.append(os.path.abspath(__file__ + '/../' * 1))
from logs import *

# PRIMITIVE OPERATIONS
def t(*args):
    return type(*args)

def bl(x, Y):
    from var import *
    if not isinstance(x, type) and isinstance(Y, type):
        if isinstance(x, Y):
            return True
        return False
    elif is_cont(Y):
        return x in Y
    else:
        err(f'Y must be a type or a container.')

def sm(x, y):
    return x is y

def eq(x, y):
    if sm(t(x), t(y)):
        if isinstance(x, type) or isinstance(y, type):
            if sm(x, y):
                return True
            return False
        return x == y
    err(f'The variables {x} and {y} must have the same type.')

def lt(x, y):
    if sm(t(x), t(y)):
        if isinstance(x, type) and isinstance(y, type):
            return issubclass(x, y)
        elif isinstance(x, str) and isinstance(y, str):
            return bl(x, y)
        elif isinstance(x, list) and isinstance(y, list):
            return any((x[i:i + len(y)] == y) for i in range(len(x) - len(y) + 1))
        elif isinstance(x, tuple) and isinstance(y, tuple):
            return any((x[i:i + len(y)] == y) for i in range(len(x) - len(y) + 1))
        elif isinstance(x, set) and isinstance(y, set):
            return x < y
        try:
            return x < y
        except:
            err(f'The type {t(x)} can not be compared.')
    else:
        err(f'The variables {x} and {y} must have the same type.')

def le(x, y):
    if lt(x, y) or eq(x, y):
        return True
    return False

# NEGATIVES
def n(f):
    if callable(f):
        def n_f(*args, **kwargs):
            return not f(*args, **kwargs)
        return n_f
    return not f

nbl = n(bl)
nb = nbl
neq = n(eq)
ne = neq
gt = n(le)
ge = n(lt)


# NULLITY
def nill(*args, **kargs):
    pass

def id_(x):
    return x

def null_(t):
    if sm(t, int):
        return 0
    elif sm(t, float):
        return 0.0
    elif sm(t, str):
        return ""
    elif sm(t, list):
        return []
    elif sm(t, dict):
        return {}
    elif sm(t, set):
        return set()
    elif sm(t, tuple):
        return ()
    elif sm(t, types.FunctionType):
        return nill
    else:
        return None

def null(x):
    return null_(t(x))

def nl(x):
    if eq(x, null(x)):
        return True
    return False
nnl = n(nl)
nn = nnl
