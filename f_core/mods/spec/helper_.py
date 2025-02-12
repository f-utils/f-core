def n_(func):
    def n_func(*args):
        return not func(*args)
    return n_func

def curry_(f, x):
    if not isinstance(x, tuple):
        raise TypeError(f'{x} is not a tuple.')
    return lambda *args: f(*x, *args)

def inter_seq(*seqs):
    return [item for item in seqs[0] if all(seq[i] == item for seq in seqs for i in range(len(seq)) if i < len(seqs[0]))]

def inter_cont(*conts):
    return set(conts[0]).intersection(*conts[1:])
