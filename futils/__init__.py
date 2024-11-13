from futils.core import *
from futils.mods import re as R
from futils.mods import path as P
from futils.mods import json as J
from futils.mods import http as H
from futils.mods import sub as S


# error classes
class ReErr(Exception):
    pass
class PathErr(Exception):
    pass
class JsonErr(Exception):
    pass
class HttpErr(Exception):
    pass
class SubErr(Exception):
    pass
