from f_core.mods.type.main_ import StrucTypes as struc

class Sub:
    @staticmethod
    def seq(x, y, same_type=True):
        if same_type and type(x) is not type(y):
            raise TypeError(f"'{x}' and '{y}' must be of the same_type type.")
        if not isinstance(x, struc.Sequence) or not isinstance(y, struc.Sequence):
            raise TypeError(f"Both '{x}' and '{y}' must be sequence objects.")
        if len(x) == 0:
            return True
        if len(x) > len(y):
            return False
        return any(y[i:i+len(x)] == x for i in range(len(y) - len(x) + 1))

    @staticmethod
    def sized(x, y, same_type=True):
        if same_type and type(x) is not type(y):
            raise TypeError(f"'{x}' and '{y}' must be of the same_type type.")
        if not isinstance(x, struc.Sized) or not isinstance(y, struc.Sized):
            raise TypeError(f"Both '{x}' and '{y}' must be sized objects.")
        return len(x) < len(y)

    @staticmethod
    def hash(x, y, same_type=True):
        if same_type and type(x) is not type(y):
            raise TypeError(f"'{x}' and '{y}' must be of the same_type type.")
        if not isinstance(x, struc.Hashable) or not isinstance(y, struc.Hashable):
            raise TypeError(f"Both '{x}' and '{y}' must be hashable objects.")
        return hash(x) < hash(y)

    @staticmethod
    def cont(x, y, same_type=True):
        if same_type and type(x) is not type(y):
            raise TypeError(f"'{x}' and '{y}' must be of the same_type type.")
        if not isinstance(x, struc.Container) or not isinstance(y, struc.Container):
            raise TypeError(f"Both '{x}' and '{y}' must be conttainer objects.")
        return all(item in y for item in x)

    @staticmethod
    def iter(x, y, same_type=True):
        if same_type and type(x) is not type(y):
            raise TypeError(f"'{x}' and '{y}' must be of the same_type type.")
        if not isinstance(x, struc.Iterable) or not isinstance(y, struc.Iterable):
            raise TypeError(f"Both '{x}' and '{y}' must be iterable objects.")
        x_iter = iter(x)
        y_iter = iter(y)
        try:
            x_item = next(x_iter)
            for y_item in y_iter:
                if x_item == y_item:
                    x_item = next(x_iter, None)
                if x_item is None:
                    return True
            return False
        except StopIteration:
            return True

    @staticmethod
    def map(x, y, same_type=True):
        if same_type and type(x) is not type(y):
            raise TypeError(f"'{x}' and '{y}' must be of the same type.")
        if not isinstance(x, struc.Mapping) or not isinstance(y, struc.Mapping):
            raise TypeError(f"Both '{x}' and '{y}' must be mapping objects.")
        return all(item in y.items() for item in x.items())
