def is_subseq(x, y):
    if len(x) == 0:
        return True
    if len(x) > len(y):
        return False
    return any(y[i:i+len(x)] == x for i in range(len(y) - len(x) + 1))

def is_subsized(x, y):
    return len(x) < len(y)

def is_subcont(x, y):
    return all(item in y for item in x)

def is_subiter(x, y):



