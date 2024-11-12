import sys, os
sys.path.append(os.path.abspath(__file__ + '/../' * 1))
import futils.core.op as op
from futils.core.logs import *
import futils.core.ty as ty
import inspect
import types

def signature(f):
    if callable(f):
        return inspect.signature(f)
    else:
        op.err(f'{f} is not a callable entity.')

def entries(f):
    if callable(f):
        return tuple(x for x in signature(f).parameters.keys())
    else:
        op.err(f'{f} is not a callable entity.')

def domain(f):
    if callable(f):
        return tuple(
            param.annotation
            for var, param in inspect.signature(f).parameters.items()
            if param.annotation is not inspect._empty
        )
    else:
        op.err(f'{f} is not a callable entity.')
dom = domain

def codomain(f):
    if callable(f):
        return signature(f).return_annotation
    else:
        op.err(f'{f} is not a callable entity.')

def compose(*functions):
    for f in functions:
        if not callable(f):
            op.err(f'{f} is not a callable entity.')
    def compose_operation(f, g):
        return lambda x: g(f(x))
    composed_function = functions[0]
    for func in functions[1:]:
        if op.lt(codomain(composed_function), domain(func)):
            composed_function = compose_operation(composed_function, func)
        else:
            op.err(f'The target of {composed_function} is not '
                   f'a subclass of the domain of {func}.')
    return composed_function
comp = compose

# extending the original "lt" function
def lt(f, g):
    if callable(f) and callable(g):
        if op.eq(entries(f), entries(g)):
            return op.lt(f(*entries(f)), g(*entries(g)))
    else:
        op.lt(f, g)

# extending the original "prod" function
def prod(*entries):
    for f in entries:
        if not callable(f):
            return ty.prod(*entries)

    def combined_func(tup):
        return tuple(func(x) for func, x in zip(entries, tup))
    return combined_func

# extending the original "coprod" function
def coprod(*entries):
    for f in entries:
        if not callable(f):
            return type.coprod(*entries)
    def combined_func(x):
        for f in entries:
            if op.bl(x, domain(f)):
                return f(x)
    return combined_funcg
