from f_core.mods.glob.sub_ import Sub as sub
from itertools import product

def n_(func):
    def n_func(*args):
        return not func(*args)
    return n_func

def curry_(f, x):
    if not isinstance(x, tuple):
        raise TypeError(f'{x} is not a tuple.')
    return lambda *args: f(*x, *args)

def join_str(str1, str2):
    return ''.join([str1, str2])

def join_list(list1, list2):
    return list1.extend(list2) or list1

def join_tuple(tuple1, tuple2):
    return tuple1.__add__(tuple2)

def join_set(set1, set2):
    return set1.union(set2)

def join_dict(dict1, dict2):
    combined_dict = dict1.copy()
    combined_dict.update(dict2)
    return combined_dict

def inter_str(*strings):
    return ''.join(char for i, char in enumerate(strings[0]) if all(i < len(string) and char == string[i] for string in strings[1:]))

def inter_tuple(*seqs):
    if not seqs:
        return tuple()
    return tuple(item for item in seqs[0] if all(item in seq for seq in seqs))

def inter_list(*seqs):
    if not seqs:
        return []
    return list(item for item in seqs[0] if all(item in seq for seq in seqs))

def inter_set(*conts):
    return set(conts[0]).intersection(*conts[1:])

def inter_dict(*dicts):
    return { key: dicts[0][key] for key in dicts[0].keys() if all(key in d and dicts[0][key] == d[key] for d in dicts[1:])}

def filter_list(X, *funcs):
    filtered_list = []
    for x in X:
        try:
            if all(f(x) for f in funcs):
                filtered_list.append(x)
        except:
            continue
    return filtered_list

def filter_tuple(X, *funcs):
    filtered_tuple = []
    for x in X:
        try:
            if all(f(x) for f in funcs):
                filtered_tuple.append(x)
        except:
            continue
    return tuple(filtered_tuple)

def filter_set(X, *funcs):
    filtered_set = []
    for x in X:
        try:
            if all(f(x) for f in funcs):
                filtered_set.append(x)
        except:
            continue
    return set(filtered_set)

def filter_str(X, *funcs):
    filtered_str = ''
    for x in X:
        try:
            if all(f(x) for f in funcs):
                filtered_str += x
        except:
            continue
    return filtered_str

def filter_dict(X, *funcs):
    filtered_dict = {}
    for k, v in X.items():
        try:
            if all(f((k, v)) for f in funcs):
                filtered_dict[k] = v
        except:
            continue
    return filtered_dict

def compl_list(X, A):
    if sub.seq(A, X):
        return [x for x in X if x not in A]
    raise AttributeError(f'{A} is not a subsequence of {X}.')

def compl_tuple(X, A):
    if sub.seq(A, X):
        return tuple(x for x in X if x not in A)
    raise AttributeError(f'{A} is not a subsequence of {X}.')

def compl_dict(X, A):
    if sub.map(A, X):
        return {k: v for k, v in X.items() if k not in A}
    raise AttributeError(f'{A} is not a submapping of {X}.')

def compl_set(X, A):
    if sub.cont(A, X):
        return {x for x in X if x not in A}
    raise AttributeError(f'{A} is not a subcontainer of {X}.')

def compl_str(X, A):
    if sub.seq(A, X):
        return ''.join(x for x in X if x not in A)
    raise AttributeError(f'{A} is not a subsequence of {X}.')


def prod_str(x, y):
    return [''.join(pair) for pair in itertools.product(x, y)]

def prod_tuple(X, Y):
    return tuple(product(X, Y))

def prod_list(X, Y):
    return list(product(X, Y))

def prod_set(X, Y):
    return set(product(X, Y))

def prod_dict(X, Y):
    return {(k1, k2): (v1, v2) for k1, v1 in X.items() for k2, v2 in Y.items()}
