import sys, os
sys.path.append(os.path.abspath(__file__ + '/../' * 1))
from logs import *
from op import *

# BY KINDS
def is_iterable(x):
    from collections.abc import Iterable
    return bl(x, Iterable)
is_iter = is_iterable

def is_container(x):
    from collections.abc import Container
    return bl(x, Container)
is_cont = is_container

def is_hash(x):
    try:
        hash(x)
        return True
    except:
        return False

def is_mutable(x):
    if bl(x, (int, float, str, tuple, frozenset, bytes)):
        return False
    elif isinstance(x, (list, dict, set, bytearray)):
        return True
    else:
        return None
is_mut = is_mutable

def is_callable(x):
    return callable(x)
is_call = is_callable

# BY SCOPE
def is_local(x):
    if bl(x, locals()):
        return True
    return False
is_loc = is_local

def is_global(x):
    if bl(x, globals()):
        return True
    return False
is_glo = is_global

def is_nonlocal(x):
    if is_local(x) or is_global(x):
        return False
    return True
is_nloc = is_nonlocal

