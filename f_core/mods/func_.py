from f import f

f.s.i(
    'curry_',
    'a general curry function',
    lambda *args: f'The variables are not functions nor accessible types.'
)

def _curry(f, x):
    if isinstance(x, tuple):
        return lambda *args: f(*x, *args)
    else:
        return lambda *args: f(x, *args)

# f.s.e(
#     'curry_',
#     (f.func, tuple),
#     _curry
# )

#print(f.s.info('curry_'))

