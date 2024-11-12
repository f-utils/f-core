from futils.core.logs import *
from futils.core.op import *

def add(*args, pos='right'):
    if len(args) < 2:
        err("At least two arguments must be provided: elements and the target iterable.")
    *values, target = args
    def handle_sequence(target, values, pos):
        for value in values:
            if bl(value, (list, tuple, set)):
                if pos == 'right':
                    target.extend(value)
                elif pos == 'left':
                    target = list(value) + target
                elif bl(pos, int) and ge(pos, 0):
                    if gt(pos, len(target)):
                        pos = len(target)
                    target = target[:pos] + list(value) + target[pos:]
                else:
                    err('The pos varibale must be a positive integer or "left"/"right".')
            else:
                if pos == 'right':
                    target.append(value)
                elif pos == 'left':
                    target = [value] + target
                elif bl(pos, int) and ge(pos, 0):
                    if gt(pos, len(target)):
                        pos = len(target)
                    target = target[:pos] + [value] + target[pos:]
                else:
                    err('The position must be a positive integer or "left"/"right".')
        return target

    if bl(target, list):
        target = handle_sequence(target, values, pos)
    elif bl(target, set):
        for value in values:
            if is_iter(value) and nb(value, (str, bytes)):
                target.update(value)
            else:
                target.add(value)
    elif bl(target, tuple):
        target_list = list(target)
        target_list = handle_sequence(target_list, values, pos)
        target = tuple(target_list)
    else:
        err(f"{target} must be a list, set, or tuple.")
    return target

def keys(x):
    return x.keys()

def values(x):
    return x.values()
vals = values

def items(x):
    return x.items()

def enum(x):
    return enumerate(x)

def get_keys(x):
    keys_list = []
    for k in keys(x):
        add(k, keys_list)
    return keys_list
gk = get_keys

def dimension(x):
    if bl(x, (int, float, str)):
        return 0
    elif bl(x, (list, tuple, set)):
        if n(x):
            return 0
        return 1 + max(dimension(item) for item in x)
    elif bl(x, dict):
        if n(x):
            return 0
        max_value_dim = max(dimension(v) for v in values(x))
        max_key_dim= max(dimension(k) for k in keys(x))
        return 1 + max(max_value_dim, max_key_dim)
    return 0
dim = dimension

def get_values_depth(data, start_depth=0):
    if nb(data, (dict, list)):
        return [(data, current_depth)], current_depth

    deepest_values = []
    max_depth = start_depth

    if bl(data, dict):
        for key, value in items(data):
            values, depth = get_values_depth(value, start_depth + 1)
            if gt(depth, max_depth):
                deepest_values = values
                max_depth = depth
            elif eq(depth,  max_depth):
                add(values, deepest_values)

    elif bl(data, list):
        for item in data:
            values, depth = get_values_depth(item, start_depth + 1)
            if gt(depth, max_depth):
                deepest_values = values
                max_depth = depth
            elif eq(depth, max_depth):
                add(values, deepest_values)
    return deepest_values
gvd = get_values_depth

def get_values(data):
    values = gvd(data)
    return [value for value in values]
gv = get_values

def index(x, Y):
    index_map = {element: index for index, element in enumerate(Y)}
    return index_map.get(x, None)
ind = index

def to_str(x, separator=', '):
    return separator.join(map(str, x))
tostr = to_str
ts = tostr

def serialize(x):
    if bl(x, (int, str, bool, type(None))):
        return x
    elif bl(x, float):
        return str(x)
    elif bl(x, dict):
        return {k: serialize(v) for k, v in items(x)}
    elif bl(x, list):
        return [serialize(i) for i in x]
    else:
        return str(x)
ser = serialize

def flat(x):
    flat_list = []
    for item in nested_lists:
        if bl(item, list):
            add(flat(x), flat_list)
        else:
            add(x, flat_list)
    return flat_list
