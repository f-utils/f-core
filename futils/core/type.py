import sys, os
sys.path.append(os.path.abspath(__file__ + '/../' * 1))
from logs import *
from op import *

# def prod(*args)

# def coprod(*args)

def name(x):
    return x().__class__.__name__
