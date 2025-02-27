```
  /$$$$$$                                             
 /$$__  $$                                            
| $$  \__/      /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$ 
| $$$$ /$$$$$$ /$$_____/ /$$__  $$ /$$__  $$ /$$__  $$
| $$_/|______/| $$      | $$  \ $$| $$  \__/| $$$$$$$$
| $$          | $$      | $$  | $$| $$      | $$_____/
| $$          |  $$$$$$$|  $$$$$$/| $$      |  $$$$$$$
|__/           \_______/ \______/ |__/       \_______/                                                  
```

# About

`f-core` is the core lib of `f-utils`. It provides the primitive accessible types, type operations and spectra.

# Structure

```
f_core/
  |-- __init__.py ........ import main.py 
  |-- main.py ............ import the modules and define classes s, t, o and g
  `-- mods/
       |-- type/ ......... define the primitive types
       |-- op/ ........... define the primitive type operations
       |-- spec/ ......... define the primitive spectra
       `-- glob/ ......... define the primitive globals
```

# Dependencies

1. `python >= 3.9`
2. `f-utils/f`

# Install

Through the `main` and `dev` branches of this repo:

* With `pip`:
```bash
# main branch
/path/to/venv/bin/pip install git+https://github.com/f-utils/f-core
# dev branch
/path/to/venv/bin/pip install git+https://github.com/f-utils/f-core/tree/dev
```

For other installation options, see [futils.org/install](https://futils.org/docs/libs/install).

# Usage

We recommend to include `f-core` directly:

```python
from f_core import *
```

This will provide the following classes:

```
class      alias    scope
-------------------------------------------
Types      t        primitive types
Ops        o        primite type operations
Globals    g        primite globals
Specs      s        primitive spectra
```

For more details, see [futils.org/libs/f-core](https://futils.org/libs/f-core).

# License

This software is [licensed](./LICENSE) under BSD.
