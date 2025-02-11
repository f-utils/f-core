from types import FunctionType, LambdaType
import inspect
from collections.abc import MutableSequence, MutableMapping, MutableSet
from f_core.mods.glob.sub_ import Sub
from f_core.mods.type.main_ import StrucTypes as struc

class Is:
    aliases = {
        'type':  ['t'],
        'call':  ['callable', 'c'],
        'func':  ['f', 'function'],
        'lamb':  ['l'],
        'cont':  ['container', 'cnt'],
        'sized': ['sized', 'szd'],
        'iter':  ['iterable', 'i', 'it'],
        'seq':   ['sequence', 'sequencial', 'sq'],
        'hash':  ['hashable', 'h'],
        'dyn':   ['dynamic', 'd', 'mutable', 'mut'],
        'empty': ['e'],
        'sing':  ['sg', 'singleton'],
        'null':  ['zero', 'n', 'z'],
        'map':   ['m', 'mapping'],
        'app':   ['a', 'append', 'appendable']
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
            return issubclass(x, struc.Call)
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
            return issubclass(x, struc.Cont)
        return isinstance(x, struc.Cont)

    @staticmethod
    def sized(x):
        if isinstance(x, type):
            return issubclass(x, struc.Sized)
        return isinstance(x, struc.Sized)

    @staticmethod
    def iter(x):
        if isinstance(x, type):
            return issubclass(x, struc.Iter)
        return isinstance(x, struc.Iter)

    @staticmethod
    def seq(x):
        if isinstance(x, type):
            return issubclass(x, struc.Seq)
        return isinstance(x, struc.Seq)

    @staticmethod
    def hash(x):
        if isinstance(x, type):
            return issubclass(x, struc.Hash)
        return isinstance(x, struc.Hash)

    @staticmethod
    def map(x):
        if isinstance(x, type):
            return issubclass(x, struc.Map)
        return isinstance(x, struc.Map)

    @staticmethod
    def app(x):
        if isinstance(x, type):
            return issubclass(x, struc.App)
        return isinstance(x, struc.App)

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
    def sing(x):
        if not isinstance(x, (struc.Sized, struc.Cont)):
            return False
        return len(x) == 1

    @staticmethod
    def null(x):
        if isinstance(x, type):
            return issubclass(x, struc.Nullable)
        if isinstance(x, (int, float, complex)):
            return x == 0
        if isinstance(x, struc.Nullable):
            return x.__null__

    for base_name, alias_list in aliases.items():
        _func = locals()[base_name]
        for alias in alias_list:
            locals()[alias] = _func
