import inspect
from typing import get_type_hints
from f import f
from f_core.mods.utils import flat_, func_instance_

# TODO
class Func:
    """
    The class of 'functions':
        1. objects are callable
        2. defined composition
    """
    pass

# TODO
class DomRuntimedFunc:
    """
    The class of 'domain-runtimed functions':
        1. defined domain (at runtime)
        2 defined composition
    It is a subclass of 'Func'
    """
    pass

# TODO
class CodRuntimedFunc:
    """
    The class of 'codomain-runtimed functions':
        1. defined codomain (at runtime)
        2. defined composition
    It is a subclass of 'Func'
    """
    pass

# TODO
class RuntimedFunc:
    """
    The class of 'runtimed functions':
        1. defined domain and codomain (at runtime)
        2. safe composition (checked at runtime)
    It is a subclass of:
        1. 'DomRuntimedFunc'
        2. 'CodRuntimedFunc'
    """
    pass

# TODO
class DomHintedFunc:
    """
    The class of 'domain-hinted functions':
        1. defined domain (based on type hints)
        2. defined composition
    It is a subclass of 'Func'
    """
    pass

# TODO
class CodHintedFunc:
    """
    The class of 'codomain-hinted functions':
        1. defined codomain (based on type hints)
        2. defined composition
    It is a subclass of 'Func'
    """
    pass

# TODO
class HintedFunc:
    """
    The class of 'hinted functions':
        1. have type hints
        2. defined domain and codomain (based on type hints)
        3. safe composition (based on type hints)
    It is a subclass of:
        1. 'DomHintedFunc'
        2. 'CodHintedFunc'
    """
    pass

# TODO
class DomTypedFunc:
    """
    The class of 'domain-typed functions':
        1. defined and checked domain
        2. defined composition
    It is a subclass of:
        1. 'DomHintedFunc'
        2. 'DomRuntimedFunc'
    """
    pass

# TODO
class CodTypedFunc:
    """
    The class of 'codomain-hinted functions':
        1. defined and checked codomain
        2. defined composition
    It is a subclass of:
        1. 'CodHintedFunc'
        2. 'CodRuntimedFunc'
    """
    pass

# TODO: refactor according to the above descriptions
class TypedFunc:
    """
    The class of 'typed functions':
        1. have type hints
        2. type hints are checked at runtime
        3. defined domain and codomain (based on type hints)
        4. safe composition (based on type hints)
    It is a subclass of:
        1. 'DomTypedFunc'
        2. 'CodTypedFunc'
        3. 'RuntimedFunc'
        4. 'HintedFunc'
    """
    def __init__(self, func):
        if not callable(func):
            raise TypeError(f"'{func}' is not a function.")
        self.func = func
        self._type_hints = get_type_hints(func)
        if not self._type_hints:
            raise TypeError(f"The function '{func.__name__}' lacks type hints.")
        self._domain = self.get_domain()
        self._codomain = self.get_codomain()

    def get_domain(self):
        type_hints = get_type_hints(self.func)
        domain_hints = tuple(type_hints.values())[:-1]
        if domain_hints:
            return Builder.prod_type_(*domain_hints)
        return type(None)

    def get_codomain(self):
        type_hints = get_type_hints(self.func)
        return_hint = list(type_hints.values())[-1]
        if return_hint:
            return return_hint
        return type(None)

    @property
    def domain(self):
        return self._domain

    @property
    def codomain(self):
        return self._codomain

    def __call__(self, *args, **kwargs):
        bound_args = inspect.signature(self.func).bind(*args, **kwargs)
        bound_args.apply_defaults()

        for arg_name, arg_value in bound_args.arguments.items():
            if arg_name in self._type_hints:
                expected_type = self._type_hints[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(f"Argument '{arg_name}' is not of type '{expected_type.__name__}'.")
        try:
            result = self.func(*args, **kwargs)
        except Exception as e:
            raise TypeError(f"Function '{self.func.__name__}' raised an error: {e}")

        if 'return' in self._type_hints:
            expected_return_type = self._type_hints['return']
            if not isinstance(result, expected_return_type):
                raise TypeError(f"Return '{result}' is not of type '{expected_return_type.__name__}'.")

        return result

    def __mul__(self, other):
        if not isinstance(other, TypedFunc):
            raise TypeError(f"'{other}' is not a valid typed function.")

        if not issubclass(other.codomain, self.domain):
            raise TypeError(f"Codomain '{other.codomain.__name__}' of '{other.func.__name__}' is not a subtype of the domain '{self.domain.__name__}' of '{self.func.__name__}'.")

        def comp(*args, **kwargs):
            return self.func(other.func(*args, **kwargs))

        return TypedFunc(comp)
