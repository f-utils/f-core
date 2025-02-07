from collections.abc import Iterable, Container, Sequence
from types import FunctionType, LambdaType
import inspect
from collections.abc import MutableSequence, MutableMapping, MutableSet

class Is:
    aliases = {
        'type':  ['t', 'class'],
        'call':  ['callable', 'c'],
        'func':  ['f', 'function'],
        'lamb':  ['l'],
        'cont':  ['container', 'C'],
        'iter':  ['iterable', 'i'],
        'seq':   ['sequence', 'sequencial', 's'],
        'hash':  ['hashable', 'h'],
        'dyn':   ['dynamic', 'd', 'mutable', 'm']
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
        return callable(x)

    @staticmethod
    def func(x):
        return isinstance(x, FunctionType)

    @staticmethod
    def lamb(x):
        return isinstance(x, LambdaType)

    @staticmethod
    def cont(x):
        return isinstance(x, Container)

    @staticmethod
    def iter(x):
        return isinstance(x, Iterable)

    @staticmethod
    def seq(x):
        return isinstance(x, Sequence)

    @staticmethod
    def hash(x):
        try:
            hash(x)
            return True
        except:
            return False

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

    for base_name, alias_list in aliases.items():
        _func = locals()[base_name]
        for alias in alias_list:
            locals()[alias] = _func
