import inspect
from typing import get_type_hints
from f import f
from f_core.mods.type.helper_ import (
        runtime_domain,
        runtime_codomain,
        runtime_comp,
        hinted_domain,
        hinted_codomain,
        hinted_comp,
        check_domain,
        check_codomain,
        typed_comp
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
        if not callable(func):
            raise TypeError(f"'{func}' is not callable.")
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __mul__(self, other):
        if not isinstance(other, PlainFunc):
            raise TypeError(f"'{other}' is not a valid plain function.")
        def comp(*args, **kwargs):
            return self.func(other(*args, **kwargs))
        return PlainFunc(comp)


# -----------------------------
#       Runtimed Functions
# -----------------------------
class RuntimedDomFunc(PlainFunc):
    """
    The class of 'domain-runtimed functions':
        1. defined domain (at runtime)
        2 defined comp
    It is a subclass of 'PlainFunc'
    """
    def __init__(self, func):
        super().__init__(func)
        self._runtime_domain = runtime_domain(func)

    @property
    def domain(self):
        return self._runtime_domain

class RuntimedCodFunc:
    """
    The class of 'codomain-runtimed functions':
        1. defined codomain (at runtime)
        2. defined comp
    It is a subclass of 'PlainFunc'
    """
    def __init__(self, func):
        super().__init__(func)
        self._runtime_codomain = runtime_codomain(func)

    @property
    def codomain(self):
        return self._runtime_codomain

class RuntimedFunc:
    """
    The class of 'runtimed functions':
        1. defined domain and codomain (at runtime)
        2. safe comp (checked at runtime)
    It is a subclass of:
        1. 'DomRuntimedFunc'
        2. 'CodRuntimedFunc'
    """
    def __init__(self, func):
        RuntimedDomFunc.__init__(self, func)
        RuntimedCodFunc.__init__(self, func)

    def __mul__(self, other):
        if not isinstance(other, RuntimedFunc):
            raise TypeError(f"'{other}' is not a valid runtimed function.")

        comp_func = runtime_comp(self, other)
        return RuntimedFunc(comp_func)


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
        super().__init__(func)
        self._hinted_domain = hinted_domain(func)

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
        super().__init__(func)
        self._hinted_codomain = hinted_codomain(func)

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
        HintedDomFunc.__init__(self, func)
        HintedCodFunc.__init__(self, func)

    def __mul__(self, other):
        if not isinstance(other, HintedFunc):
            raise TypeError(f"'{other}' is not a valid hinted function.")

        comp_func = hinted_comp(self, other)
        return HintedFunc(comp_func)


# ---------------------------
#       Typed Functions
# ---------------------------
class TypedDomFunc(HintedDomFunc, RuntimedDomFunc):
    """
    The class of 'domain-typed functions':
        1. defined and checked domain
        2. defined comp
    It is a subclass of:
        1. 'HintedDomFunc'
        2. 'RuntimedDomFunc'
    """
    def __init__(self, func):
        HintedDomFunc.__init__(self, func)
        RuntimedDomFunc.__init__(self, func)
        check_domain(func)

    @property
    def domain(self):
        return self._hinted_domain

    def __call__(self, *args, **kwargs):
        check_domain(self.func)
        return super().__call__(*args, **kwargs)


class TypedCodFunc(HintedCodFunc, RuntimedCodFunc):
    """
    The class of 'codomain-typed functions':
        1. defined and checked codomain
        2. defined comp
    It is a subclass of:
        1. 'CodHintedFunc'
        2. 'CodRuntimedFunc'
    """
    def __init__(self, func):
        HintedCodFunc.__init__(self, func)
        RuntimedCodFunc.__init__(self, func)
        check_codomain(func)

    @property
    def codomain(self):
        return self._hinted_codomain

    def __call__(self, *args, **kwargs):
        result = super().__call__(*args, **kwargs)
        check_codomain(self.func)
        return result


class TypedFunc(TypedDomFunc, TypedCodFunc, RuntimedFunc, HintedFunc):
    """
    The class of 'typed functions':
        1. have type hints
        2. type hints are checked at runtime
        3. defined domain and codomain (based on type hints)
        4. safe comp (based on type hints)
    It is a subclass of:
        1. 'TypedDomFunc'
        2. 'TypedCodFunc'
        3. 'RuntimedFunc'
        4. 'HintedFunc'
    """
    def __init__(self, func):
        if not callable(func):
            raise TypeError(f"'{func}' is not a function.")
        super().__init__(func)

    def __call__(self, *args, **kwargs):
        check_domain(self.func)
        try:
            result = self.func(*args, **kwargs)
        except Exception as e:
            raise TypeError(f"Function '{self.func.__name__}' raised an error: {e}")
        check_codomain(self.func)

        return result

    def __mul__(self, other):
        if not isinstance(other, TypedFunc):
            raise TypeError(f"'{other}' is not a valid typed function.")

        comp_func = typed_comp(self, other)
        return TypedFunc(comp_func)
