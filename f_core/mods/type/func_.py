import inspect
from typing import get_type_hints
from functools import wraps
from f import f
from types import FunctionType, LambdaType
from f_core.mods.type.helper_ import (
    is_domain_hinted,
    is_codomain_hinted,
    hinted_domain,
    hinted_codomain,
    runtime_domain,
    runtime_codomain,
    check_domain,
    check_codomain
)

# -----------------------------
#       Plain Functions
# -----------------------------
class PlainFunc:
    """
    The class of 'plain functions':
        1. objects are callable
        2. defined comp
    """
    def __init__(self, func):
        if type(func) is not FunctionType or type(func) is not LambdaType:
            raise TypeError(f"'{func}' is not a function nor a lambda.")
        self.func = func
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __mul__(self, other):
        if not isinstance(other, PlainFunc):
            raise TypeError(f"'{other}' is not a valid plain function.")
        def comp(*args, **kwargs):
            return self.func(other(*args, **kwargs))
        return PlainFunc(comp)


# -------------------------
#     Hinted Functions
# -------------------------
class HintedDomFunc(PlainFunc):
    """
    The class of 'domain-hinted functions':
        1. defined domain (based on type hints)
        2. defined comp
    It is a subclass of 'PlainFunc'
    """
    def __init__(self, func):
        is_domain_hinted(func)
        super().__init__(func)
        self._hinted_domain = hinted_domain(func)
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        is_domain_hinted(self.func)
        return super().__call__(*args, **kwargs)

    @property
    def domain(self):
        return self._hinted_domain


class HintedCodFunc(PlainFunc):
    """
    The class of 'codomain-hinted functions':
        1. defined codomain (based on type hints)
        2. defined comp
    It is a subclass of 'PlainFunc'
    """
    def __init__(self, func):
        is_codomain_hinted(func)
        super().__init__(func)
        self._hinted_codomain = hinted_codomain(func)
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        is_codomain_hinted(self.func)
        return super().__call__(*args, **kwargs)

    @property
    def codomain(self):
        return self._hinted_codomain


class HintedFunc(HintedDomFunc, HintedCodFunc):
    """
    The class of 'hinted functions':
        1. have type hints
        2. defined domain and codomain (based on type hints)
        3. safe comp (based on type hints)
    It is a subclass of:
        1. 'HintedDomFunc'
        2. 'HintedCodFunc'
    """
    def __init__(self, func):
        is_domain_hinted(func)
        is_codomain_hinted(func)
        HintedDomFunc.__init__(self, func)
        HintedCodFunc.__init__(self, func)
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        is_domain_hinted(self.func)
        is_codomain_hinted(self.func)
        return super().__call__(*args, **kwargs)

    def __mul__(self, other):
        if not isinstance(other, HintedFunc):
            raise TypeError(f"'{other}' is not a valid hinted function.")

        comp_func = safe_comp(self, other)
        return HintedFunc(comp_func)


# ---------------------------
#       Typed Functions
# ---------------------------
class TypedDomFunc(HintedDomFunc):
    """
    The class of 'domain-typed functions':
        1. defined and checked domain
        2. defined comp
    It is a subclass of:
        1. 'HintedDomFunc'
    """
    def __init__(self, func):
        is_domain_hinted(func)
        HintedDomFunc.__init__(self, func)
        self.func = func
        self.hinted_domain = hinted_domain(func)
        self.runtime_check_domainer = runtime_domain(func)
        self.param_names = list(inspect.signature(func).parameters.keys())
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        is_domain_hinted(self.func)
        expected_types = self.hinted_domain
        actual_types = tuple(map(type, args))
        check_domain(self.func, self.param_names, expected_types, actual_types)
        return super().__call__(*args, **kwargs)

    @property
    def domain(self):
        return self.hinted_domain

class TypedCodFunc(HintedCodFunc):
    """
    The class of 'codomain-typed functions':
        1. defined and checked codomain
        2. defined comp
    It is a subclass of:
        1. 'CodHintedFunc'
    """
    def __init__(self, func):
        is_codomain_hinted(func)
        super().__init__(func)
        self.hinted_codomain = hinted_codomain(func)
        check_codomain(func, self.hinted_codomain, runtime_codomain(func))
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        is_codomain_hinted(self.func)
        result = super().__call__(*args, **kwargs)
        actual_codomain = type(result)
        check_codomain(self.func, self._hinted_codomain, actual_codomain)
        return result

        @property
        def codomain(self):
            return self.hinted_codomain


class TypedFunc(TypedDomFunc, TypedCodFunc):
    """
    The class of 'typed functions':
        1. have type hints
        2. type hints are checked at runtime
        3. defined domain and codomain based on type hints
        4. safe composition (based on type hints)
    It is a subclass of:
        1. 'TypedDomFunc'
        2. 'TypedCodFunc'
        3. 'HintedFunc'
    """
    def __init__(self, func):
        if not callable(func):
            raise TypeError(f"'{func}' is not callable.")
        is_domain_hinted(func)
        is_codomain_hinted(func)
        TypedDomFunc.__init__(self, func)
        TypedCodFunc.__init__(self, func)
        self.__name__ = func.__name__

        # Use wraps to maintain function metadata
        self.func = wraps(func)(self._create_wrapped_function(func))

    def _create_wrapped_function(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            is_domain_hinted(func)
            is_codomain_hinted(func)
            result = TypedDomFunc.__call__(self, *args, **kwargs)
            actual_codomain = type(result)
            check_codomain(self.func, self._hinted_codomain, actual_codomain)
            return result
        return wrapped

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __mul__(self, other):
        if not isinstance(other, TypedFunc):
            raise TypeError(f"'{other}' is not a valid typed function.")

        def safe_comp(g, f):
            f_codomain = hinted_codomain(f.func)
            g_domain = hinted_domain(g.func)

            if not issubclass(f_codomain, g_domain):
                raise TypeError(
                    f"Hinted codomain '{f_codomain.__name__}' of '{f.__name__}' "
                    f"does not match hinted domain '{g_domain.__name__}' of '{g.__name__}'."
                )
            def comp(*args: f.hinted_domain) -> g.hinted_codomain:
                return g.func(f.func(*args))
            return TypedFunc(comp)
        return safe_comp(self, other)

    @property
    def domain(self):
        return self._hinted_domain

    @property
    def codomain(self):
        return self._hinted_codomain

class BooleanFunc(TypedFunc):
    """
    The class of 'boolean functions':
        1. are typed functions
        2. its codomain is always 'bool'
    """

    def __init__(self, func):
        super().__init__(func)
        if hinted_codomain(self.func) is not bool:
            raise TypeError(f"'{self.func.__name__}' does not have 'bool' as its return type.")

    def __instancecheck__(self, instance):
        return isinstance(instance, TypedFunc) and hinted_codomain(instance.func) == bool
