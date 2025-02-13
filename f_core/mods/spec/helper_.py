def n_(func):
    def n_func(*args):
        return not func(*args)
    return n_func

def curry_(f, x):
    if not isinstance(x, tuple):
        raise TypeError(f'{x} is not a tuple.')
    return lambda *args: f(*x, *args)

def inter_str(*strings):
    return ''.join(char for i, char in enumerate(strings[0]) if all(i < len(string) and char == string[i] for string in strings[1:]))

def inter_tuple(*seqs):
    if not seqs:
        return tuple()
    return tuple(item for item in seqs[0] if all(item in seq for seq in seqs))

def inter_list(*seqs):
    if not seqs:
        return []
    return [item for item in seqs[0] if all(item in seq for seq in seqs)]

def inter_set(*conts):
    return set(conts[0]).intersection(*conts[1:])

def inter_dict(*dicts):
    return { key: dicts[0][key] for key in dicts[0].keys() if all(key in d and dicts[0][key] == d[key] for d in dicts[1:])}
