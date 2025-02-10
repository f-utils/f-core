from collections.abc import Iterable, Container, Sequence, Hashable, Callable, Sized
from types import FunctionType, LambdaType
import inspect
from collections.abc import MutableSequence, MutableMapping, MutableSet
from f_core.mods.glob.sub_ import Sub

class Is:
    aliases = {
        'type':       ['t'],
        'call':       ['callable', 'c'],
        'func':       ['f', 'function'],
        'lamb':       ['l'],
        'cont':       ['container', 'cnt'],
        'sized':      ['sized', 'szd'],
        'iter':       ['iterable', 'i', 'it'],
        'seq':        ['sequence', 'sequencial', 'sq'],
        'hash':       ['hashable', 'h'],
        'dyn':        ['dynamic', 'd', 'mutable', 'm'],
        'empty':      ['e', 'initial'],
        'singleton':  ['sg', 'terminal'],
        'null':       ['zero', 'n', 'z']
    }

    @staticmethod
    def resolve(kind):
        for k, v in Is.aliases.items():
            if kind == k:
                return kind
            if kind in v:
                return k
        return None

    @staticmethod
    def type(x):
        return isinstance(x, type)

    @staticmethod
    def call(x):
        if isinstance(x, type):
            return issubclass(x, Callable)
        return callable(x)

    @staticmethod
    def func(x):
        return isinstance(x, FunctionType)

    @staticmethod
    def lamb(x):
        return isinstance(x, LambdaType)

    @staticmethod
    def cont(x):
        if isinstance(x, type):
            return issubclass(x, Container)
        return isinstance(x, Container)

    @staticmethod
    def sized(x):
        if isinstance(x, type):
            return issubclass(x, Sized)
        return isinstance(x, Sized)

    @staticmethod
    def iter(x):
        if isinstance(x, type):
            return issubclass(x, Iterable)
        return isinstance(x, Iterable)

    @staticmethod
    def seq(x):
        if isinstance(x, type):
            return issubclass(x, Sequence)
        return isinstance(x, Sequence)

    @staticmethod
    def hash(x):
        if isinstance(x, type):
            return issubclass(x, Hashable)
        return isinstance(x, Hashable)

    @staticmethod
    def dyn(x):
        if callable(x):
            sig = inspect.signature(x)
            for param in sig.parameters.values():
                if param.kind == inspect.Parameter.VAR_POSITIONAL:
                    return True
            return False
        if isinstance(x, (list, dict, set, bytearray)):
            return True
        if isinstance(x, (MutableSequence, MutableMapping, MutableSet)):
            return True
        return False

    @staticmethod
    def empty(x):
        if Is.sized(x) and len(x) == 0:
            return True
        return False

    @staticmethod
    def singleton(x):
        if not isinstance(obj, (Sized, Container)):
            return False
        return len(x) == 1

    @staticmethod
    def null(x):
        if isinstance(x, (int, float, complex)):
            return x == 0
        if hasattr(x, '__null__') and callable(x.__null__):
            return x.__null__()
        return False

    for base_name, alias_list in aliases.items():
        _func = locals()[base_name]
        for alias in alias_list:
            locals()[alias] = _func 
