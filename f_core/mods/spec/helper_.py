def n_(func):
    def n_func(*args):
        return not func(*args)
    return n_func

def curry_(f, x):
    if isinstance(x, tuple):
        return lambda *args: f(*x, *args)
    else:
        return lambda *args: f(x, *args)
