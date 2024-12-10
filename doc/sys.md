
Everything begins with the following entities:

```
core entities
------------------
entity       type        meaning
------------------------------------------------------------------
TYPES_       dict        store the available types
FUNCS_       list        store the spectra of available functions
```

In `futils` the functions have a *spectrum*, which caracterizes its *state*. It is a generalized version of the typical *signature* of a function in Python. It consists of a dictionary with the following entries:

```
function spectrum
-------------------
entry         type         description
--------------------------------------------------
name          str          the function name
```
