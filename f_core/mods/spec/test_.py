from f import f

f.s.i(
    'belongs_',
    'Check if something belongs to something else.',
    lambda *args, **args: 'The provided types are not acceptable for the belonging operation.'
)

f.s.e(
    'belongs_',
    (type, type),
    lambda x,y: issubclass(x, y)
)


