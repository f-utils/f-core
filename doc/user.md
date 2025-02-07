# About

In this library, we build:
1. certain fundamental types, including function types with different levels of type safety
2. a lot of type operations
3. the primitive spectra and dynamic spectra.

This is provided to the user inside two classes:

1. `f-core.t/type`: with the constructed types and type operations
2. `f-core.s/spec`: with the constructed spec and dspec

> **Remark.** We recommend the user to import the lib as `from f_core import *`. Doing that you will have three fundamental classes:
> 1. `f`: with `f` lib class
> 2. `t`: with `f-core` type class
> 3. `s`: with `f-core` spec class 

# Types

The added classes contains function classes and the `Any` class.

## Function Types

1. `PlainFunc`: with composable objects. Allow multiplication-like composition through `g*f`
2. `HintedDomFunc`: with composable objects that have type hints in its arguments. Functions have `.domain` property based on type hints.
3. `HintedCodFunc`: with composable objects that have type hints in its returning argument. Functions have `.codomain` property based on type hints.
4. `HintedFunc`: with composable objects that have type hints in both arguments and returning argument. Allow multiplication-like composition `g*f` with checking if `f.codomain` is contained in `g.domain`.
5. `TypedDomFunc`: with composable objects that have type hints in arguments and a runtime checking. Functions have `.domain` property based on type hints.
6. `TypedCodFunc`: with composable objects that have type hints in returning argument and a runtime checking. Functions have `.codomain` property based on type hints.
7. `TypedFunc`: with composable objects that have type hints in both arguments and returning, with runtime checking. Allow multiplication-like composition `g*f` with checking if `f.codomain` is contained in `g.domain`.

```
type                parent types
-----------------------------------------------------------
PlainFunc           
HintedDomFunc       PlainFunc
HintedCodFunc       PlainFunc
HintedFunc          HintedDomFunc, HintedCodFunc
TypedDomFunc        HintedDomFunc
TypedCodFunc        HintedCodFunc
TypedFunc           TypedDomFunc, TypedCodFunc, HintedFunc
```

## Any Type

The `Any` type is the type whose objects are objects of any of the accessible types. In other words `x` is an object of `Any` iff `x` is an object of some type `t` in the tuple `f.t.E().keys()` of accessible types. In sum, `f_core.t.Any` is the coproduct (see below) of `f.t.E().keys()`.

Since the accessible types can change in time, the class `Any` should change as well:
1. the current version of `Any` can be obtained through `Any.get()`;
2. the underlying tuple of the accessible types can be obtained with `Any.tuple()`.

# Operations

Recall that a *type operation* (as introduced in [systematics](https://)) is a function `F(*types)` such that:
1. the type of `t` is `type` for each `t` in `types` (i.e, its arguments are types)
2. the type of `F(*types)` is `type` for each `t` in `types` (i.e, it returns a type).

In other words, it is a function that at runtime maps types into a new type.

