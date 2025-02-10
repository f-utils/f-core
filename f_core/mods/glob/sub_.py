from collections.abc import Sequence, Sized, Container, Iterable

class Sub:
    @staticmethod
    def seq(x, y, same=True):
        if same and type(x) is not type(y):
            raise TypeError("x and y must be of the same type.")
        if not isinstance(x, Sequence) or not isinstance(y, Sequence):
            raise TypeError(f"Both '{x}' and '{y}' must be sequence objects.")
        if len(x) == 0:
            return True
        if len(x) > len(y):
            return False
        return any(y[i:i+len(x)] == x for i in range(len(y) - len(x) + 1))

    @staticmethod
    def sized(x, y, same=True):
        if same and type(x) is not type(y):
            raise TypeError("x and y must be of the same type.")
        if not isinstance(x, Sized) or not isinstance(y, Sized):
            raise TypeError(f"Both '{x}' and '{y}' must be sized objects.")
        return len(x) < len(y)

    @staticmethod
    def cont(x, y, same=True):
        if same and type(x) is not type(y):
            raise TypeError("x and y must be of the same type.")
        if not isinstance(x, Container) or not isinstance(y, Container):
            raise TypeError(f"Both '{x}' and '{y}' must be conttainer objects.")
        return all(item in y for item in x)

    @staticmethod
    def iter(x, y, same=True):
        if same and type(x) is not type(y):
            raise TypeError("x and y must be of the same type.")
        if not isinstance(x, Iterable) or not isinstance(y, Iterable):
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
