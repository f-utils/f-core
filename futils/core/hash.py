import sys, os
sys.path.append(os.path.abspath(__file__ + '/../' * 1))
from logs import *
from op import *

def truncate(number, decimal_places=2):
    str_number = str(number)
    if '.' in str_number:
        integer_part, decimal_part = str_number.split('.')
        return float(f"{integer_part}.{decimal_part[:decimal_places]}")
    else:
        return number
trunc = truncate

def mod(number, divider):
    return divmod(number, divider)

def encode(string):
    return base64.b64encode(string.encode('ascii')).decode('ascii')
enc = encode

def is_encoded(string):
    try:
        base64.b64decode(string, validate=True)
        return True
    except:
        return False
isenc = is_encoded

