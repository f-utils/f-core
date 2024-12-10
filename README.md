```
  /$$$$$$$            /$$     /$$ /$$          
 /$$__              | $$    |__/| $$          
| $$  \__//$$   /$$ /$$$$$$   /$$| $$  /$$$$$$$
| $$$$$  | $$  | $$|_  $$_/  | $$| $$ /$$_____/
| $$_/   | $$  | $$  | $$    | $$| $$|  $$$$$$ 
| $$     | $$  | $$  | $$ /$$| $$| $$ \____  $$
| $$     |  $$$$$$/  |  $$$$/| $$| $$ /$$$$$$$/
|__/      \______/    \___/  |__/|__/|_______/ 
```

# About

`futils` is a general utils Python lib made  with an emphasis in a functional and procedural point of view. This means that we rarely use classes and methods and never use objects directly, and that one focus primarily on functions. When defined, classes are endowed with static methods in order to create namespaces inside modules instead of to work as a blueprint for objects. Furthermore, some Python methods are converted to plain functions.

We adopt a constructivist and unifying approach, making use of parametric polymorphisms. We begin by redefining, generalizing and unifying the basic builtin Python operations/methods, which are then used in the construction of additional functions. This is made following a custom structure that ensure type safety since from the beginning.

> `futils` is about:
> 1. functions
> 2. unification (parametric polymorphism)
> 3. type safety
> 4. simplicity

> For more details about `futils` philosophy, see [doc/phi](./doc/phi.md)

# Structure

The utils in _futils_ appears into two categories:
1. `core`: primitive generic functions, to be called directly, without a namespace.
2. `libs`: context-based functions, consuming the core utils, to be called inside a namespace.

```
futils/
  |-- core/ ................... core utils   
  `-- libs/ ................... context-based utils
```   

# The Core

The core has no dependences. It is formed by the `futils` *primitive functions*, which are constructed from the builtin Python functions and methods.

```
futils/
  `-- core/
        |-- core.py ........... the systematics
        `-- mods/ ............. the core modules 
```

Inside `futils/core` we have a `core.py`. There, the systematics used to build the `futils` functions is defined, which is designed to simplify the creation of parametric polymorphisms with type safety (see below for more details). Inside `futils/core/mods/` we have the core modules, as follows:

```
core modules
---------------
mod            description
---------------------------------------------
ansi           definition of ansi colors
logs           definition and configuration of logs
op             generalized basic operations
cmd            basic python commands
date           functions related to date and time
hash           hashable types based functions
iter           iterable-based functions
var            tests related to variables
func           function-based operations
type           type/class-based operations
comp           generalized composite operations
```

# The Systematics

In `futils`, functions have a `spectrum`, which consists of all current function information, generalizing its Python `signature`. By definition, the function is created when one *initialize* its `spectrum`, which can be *extended* or *updated* in any posterior moment. The process involves the following *structural functions*:

```
structural functions
------------------------
name            scope
----------------------------------------------------------------
_init_          creates a function by initializing its spectrum
_extend_        extends the spectrum of a function
_update_        updates the spectrum of a function
_spec_          gets the function spectrum
```

One can think of the `spectrum` as the "state" of a function, which is defined by:
1. the acceptable variable types
2. the functions which are returned for each acceptable variable type

If called with variables of acceptable types, the corresponding returning function is returned. Else, it returns its *standard return*.

The function is *initialized* with an "empty state", which means that:
1. it has no acceptable variable types
2. it has defined its "standard return"

To *extend* a function means therefore to extend its "state" by adding:
1. a new acceptable type
2. a corresponding returning function

Similarly, to *update* a function means to update its "state" by updating:
1. its standard return
2. the returning function of an acceptable type

While initialized, functions are included in the dictionary `_FUNCS_`, which therefore represents the "global functional state" of the system.

> For more details see [doc/sys](./doc/sys.md).

# The Libs

```
lib            description
----------------------------------------------
re             regex-based functions
path           functions related to the path type
json           operations for json data/files
http           http operations
sys            opeerating system operations           
```

# Interdependence

The idea is to try to maintain a linear dependence among the utils, as below. To avoid cyclic imports we use local imports.

```
lib            imports          
----------------------------------------------
ansi           nothing
logs           ansi 
op             logs 
cmd            logs, op
date           logs, op
var            logs, op
hash           logs, op
func           logs, op
type           logs, op, func
comp           logs, op, var
iter           logs, op, str, var, comp
----------------------------------------------
lib            imports          
----------------------------------------------
re             core
path           core, re
json           core, re, path
http           core, json, path
```

# Usage

* With `git`: 
```bash
git clone https://github.com/ximenesyuri/futils /path/to/venv/lib/python3.x/site-packages/functional_utils
``` 
* With `pip`:
```bash
/path/to/venv/bin/pip3 install git+https://github.com/ximenesyuri/futils
```
* With `poetry`:
```bash
poetry add git+https://github.com/ximenesyuri/futils
```

> We suggest to import the lib as `from functional_utils import *`.

# Contributors

1. Yuri Ximenes: [github](https://github.com/ximenesyuri), [linkedin](https://linkedin.com/in/ximenesyuri)
2. Rafael David: [github](https://github.com/rdvid), [linkedin](https://www.linkedin.com/in/rdvid/)
