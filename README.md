```
  /$$$$$$$            /$$     /$$ /$$          
 /$$__  $$           | $$    |__/| $$          
| $$  \__//$$   /$$ /$$$$$$   /$$| $$  /$$$$$$$
| $$$$$  | $$  | $$|_  $$_/  | $$| $$ /$$_____/
| $$_/   | $$  | $$  | $$    | $$| $$|  $$$$$$ 
| $$     | $$  | $$  | $$ /$$| $$| $$ \____  $$
| $$     |  $$$$$$/  |  $$$$/| $$| $$ /$$$$$$$/
|__/      \______/    \___/  |__/|__/|_______/ 
```

# About

`futils` is a general utils Python lib made with an emphasis in a functional and procedural point of view. This means that we rarely use classes and methods and never use objects directly, and that one focus primarily on functions. When defined, classes are endowed with static methods in order to create namespaces inside modules instead of to work as a blueprint for objects. Furthermore, some Python methods are converted to plain functions.

We adopt a constructivist and unifying approach, making use of parametric polymorphisms. We begin by redefining, generalizing and unifying the basic builtin Python operations/methods, which are then used in the construction of additional functions. 

We ensure type safety from the beginning by making a systematic use of [ximenesyuri/safe](https://github.com/ximenesyuri/safe), which is our major dependency. Actually, `futils` can be seen as an application of `safe` to the main Python utilities. 

> In sum, `futils` is about:
> 1. functions
> 2. unification (parametric polymorphisms)
> 3. type safety (through [safe](ximenesyuri/safe))
> 4. simplicity  

> For more details about `futils` philosophy, see [doc/phi](./doc/phi.md)

# Structure

The utils in `futils` appears into two categories:
1. `core`: primitive generic functions, to be called directly, without a namespace.
2. `libs`: context-based functions, consuming the `core`, to be called inside a namespace.

```
futils/
  |-- core/ ................... core utils   
  `-- libs/ ................... context-based utils
```   

# The Core

The `core` has no dependencies. It is formed by the `futils` *primitive functions*, which are constructed from the builtin Python functions and methods.

```
futils/
  `-- core/ ................... the core modules 
```

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

# The Libs

The `libs` has a minimum of dependencies.


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
