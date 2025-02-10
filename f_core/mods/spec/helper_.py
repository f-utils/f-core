def n_(func):
    def n_func(*args):
        return not func(*args)
    return n_func
