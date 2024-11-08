import sys, os
sys.path.append(os.path.abspath(__file__ + '/../' * 1))
from logs import *
from op import *
from var import *

def comprehension(f, Y, *args, position='right'):
    if n(is_iter(Y)):
        err(f'The variable Y must be an iterable.')
    if eq(position, 'right'):
        if bl(Y, list):
            return [f(*(args + (y,))) for y in Y]
        elif bl(Y, tuple):
            return (f(*(args + (y,))) for y in Y)
        elif bl(Y, dict):
            return {f(*(args + (k,))): f(*(args + (v,))) for k, v in Y.items()}
    elif position == 'left':
        if bl(Y, list):
            return [f(*(y,) + args) for y in Y]
        elif bl(Y, tuple):
            return (f(*(y,) + args) for y in Y)
        elif bl(Y, dict):
            return {f(*(k,) + args): f(*(v,) + args) for k, v in Y.items()}
    else:
        err('The position var must be "left" or "right"')
comp = comprehension

def some(x, op=None, Y=None):
    if eq(Y, None):
        if eq(op, None):
            if is_iter(x):
                return any(x)
            else:
                return x
        else:
            if is_iter(x):
                return any(comp(op, x))
            else:
                return op(x)
    elif is_iter(Y):
        if eq(op, None):
            err(f'{op} cannot be of type None if {Y} is not.')
        else:
            if is_iter(x):
                return any(flat([comp(op, Y, i) for i in x]))
            else:
                return any(comp(op, Y, x))
    else:
        if eq(op, None):
            err(f'{op} cannot be of type None if {Y} is not.')
        else:
            if is_iter(x):
                return any([op(i, Y) for i in x])
            else:
                return any(comp(op, Y, x))

def none(x, op=None, Y=None):
    return n(some(x, op, Y))

def every(X, op=None, y=None):
    if eq(y, None):
        if eq(op, None):
            all(ev(X, id))
        all(ev(X, op))
    else:
        if ne(op, None):
            if bl(y, list) or bl(y, tuple):
                if eq(op, bl):
                    return all(ev_r(X, bl, y))
                return all(ev(X, op, y))
            return all(ev(X, op, y))
        err(f'If {op} is not set, them {y} must be not set too.')

def union(*args):
    if every(args, bl, str):
        return ''.join(args)
    elif every(args, bl, list):
        result = args[0]
        for arg in args[1:]:
            result += list(arg)
        return result
    elif every(args, bl, tuple):
        result = args[0]
        for arg in args[1:]:
            result += tuple(arg)
        return result
    elif every(args, bl, set):
        result = set()
        for arg in args:
            result = result.union(arg)
        return result
    else:
        err("All arguments must be of the same type: strings, lists, tuples, or sets")
cup = union

def intersection(*args):
    def common_segments(a, b):
        result = []
        len_a, len_b = len(a), len(b)
        for i in range(len_a):
            for j in range(len_b):
                if a[i] == b[j]:
                    k = 1
                    while (i + k < len_a) and (j + k < len_b) and a[i + k] == b[j + k]:
                        k += 1
                    if k > 1:
                        result.append(a[i:i + k])
        return result
    def common_segments_in_lists(*lists):
        result = lists[0]
        for lst in lists[1:]:
            result_segments = common_segments(result, lst)
            if result_segments:
                max_len = max(eval(result_segments, len))
                for seg in result_segments:
                    if eq(len(seg), max_len):
                       result = next(seg)
            return []
        return result

    if every(args, bl, str):
        arg_lists = [list(arg) for arg in args]
        result = common_segments_in_lists(*arg_lists)
        return ''.join(result)
    elif every(args, bl [list, tuple]):
        result = common_segments_in_lists(*args)
        return type(args[0])(result)
    elif every(args, bl, set):
        result = args[0]
        for arg in args[1:]:
            result &= arg
        return result
    else:
        err("All arguments must be of the same type: strings, lists, tuples, or sets")
cap = intersection


def lower(*args):
    def apply_lower(obj):
        if bl(obj, str):
            return obj.lower()
        elif bl(obj, list):
            return eval(obj, apply_lower)
        elif bl(obj, tuple):
            return tuple(eval(obj, apply_lower))
        elif bl(obj, set):
            return set(eval(obj, apply_lower))
        elif bl(obj, dict):
            return {apply_lower(k): apply_lower(v) for k, v in obj.items()}
        else:
            return obj
    if eq(len(args), 1):
        return apply_lower(*args)
    return eval(args, apply_lower)
# > print(lower('ASS'))
low = lower
lw = low

def upper(*args):
    def apply_upper(obj):
        if bl(obj, str):
            return obj.upper()
        elif bl(obj, list):
            return eval(obj, apply_upper)
        elif bl(obj, tuple):
            return tuple(eval(obj, apply_upper))
        elif bl(obj, set):
            return set(eval(obj, apply_upper))
        elif bl(obj, dict):
            return {apply_upper(k): apply_upper(v) for k, v in obj.items()}
        else:
            return obj
    if eq(len(args), 1):
        return apply_upper(*args)
    return eval(args, apply_lower)
# > print(upper('ass'))
upp = upper
up = upp

def strip(x):
    return x.strip()
stp = strip

def split(x, separator=' '):
    return x.split(separator)
spl = split

# slice

def replace(*args):
    def apply_replace(item, replacements):
        def recursive_replace(obj):
            if bl(obj, str):
                for s, t in replacements:
                    obj = obj.replace(s, t)
                return obj
            elif bl(obj, list):
                return eval(obj, recursive_replace)
            elif bl(obj, tuple):
                return tuple(eval(obj, recursive_replace))
            elif isinstance(obj, set):
                return set(eval(obj, recursive_replace))
            elif isinstance(obj, dict):
                return {recursive_replace(k): recursive_replace(v) for k, v in obj.items()}
            else:
                return obj
        return recursive_replace(item)

    if len(args) < 2:
        err("The function requires at least two arguments.")

    replacements, target = args[:-1], args[-1]

    replacement_rules = []
    if len(replacements) == 1:
        single_replacement = replacements[0]
        if bl(single_replacement, (list, tuple, set)):
            for item in single_replacement:
                if bl(item, (list, tuple)) and len(item) == 2:
                    replacement_rules.append(tuple(item))
                else:
                    err("Invalid format for replacement pairs.")
        elif bl(single_replacement, dict):
            replacement_rules.extend(single_replacement.items())
        elif bl(single_replacement, str):
            err("If only one replacement rule is provided, it must be a collection or dict.")
        else:
            err("Invalid format for replacement rules.")
    else:
        if len(replacements) % 2 != 0:
            err("Replacement arguments must be in pairs.")
        replacement_rules = [(replacements[i], replacements[i + 1]) for i in range(0, len(replacements), 2)]

    return apply_replace(target, replacement_rules)
rep = replace
tr = rep
