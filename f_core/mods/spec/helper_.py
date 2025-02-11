def n_(func):
    def n_func(*args):
        return not func(*args)
    return n_func

def curry_(f, x):
    if not isinstance(x, tuple):
        raise TypeError(f'{x} is not a tuple.')
    return lambda *args: f(*x, *args)
