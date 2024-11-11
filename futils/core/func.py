import inspect
from . import op
from logs import *
from . import type

def signature(f):
    return inspect.signature(f)

def target(f):
    return signature(f).return_annotation

def inputs(f):
    return tuple(x for x in inspect.signature(f).parameters.keys())

def domain(f):
    return tuple(
        param.annotation
        for var, param in inspect.signature(f).parameters.items()
        if param.annotation is not inspect._empty
    )

def c_(f, g):
    if op.lt(target(f), domain(g)):
        return lambda x: g(f(x))
    else:
        err(f'The target of {f} is not a subclass of domain of {g}.')

def lt(f, g , *args, **kargs):
    if op.sm(domain(f), domain(g)):
        return op.lt(f(*args, **kargs), g(*args, **kargs))

def prod(f, g):
    def prod_f_g(pair):
        x1, x2 = pair
        return (f(x1), g(x2))
    return prod_f_g

