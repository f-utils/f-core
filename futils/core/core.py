FUNCS_ = []
TYPES_ = {}

def new_(type_name, description):
    if type_name in TYPES_:
        raise ValueError(f"Type '{type_name}' is already registered.")

    TYPES_[type_name] = description

def init_(name, std_func):
    if any(func['name'] == name for func in FUNCS_):
        raise ValueError(f"Function '{name}' is already initialized.")

    func_structure = {
        'name': name,
        'std': std_func,
        'domain': [],
        'body': {},
        'exec': None
    }
    FUNCS_.append(func_structure)

    globals()[name] = create_executable_function(name)

def create_executable_function(name):
    def executable_function(*args, **kwargs):
        func_spec = spec_(name)
        exec_func = func_spec['exec']
        if exec_func:
            return exec_func(*args, **kwargs)
        else:
            return func_spec['std'](*args, **kwargs)
    return executable_function

def extend_(name, some_type_combination, case_func):
    func_spec = spec_(name)

    if not isinstance(some_type_combination, (list, tuple)):
        raise ValueError("some_type_combination must be a list or tuple of types.")

    for some_type in some_type_combination:
        if some_type not in TYPES_:
            raise ValueError(f"Type '{some_type}' is not registered in TYPES_.")

    if not callable(case_func):
        raise ValueError("case_func must be callable.")

    if tuple(some_type_combination) in func_spec['domain']:
        raise ValueError(f"The type combination '{some_type_combination}' is already in domain for function '{name}'.")

    func_spec['domain'].append(tuple(some_type_combination))
    func_spec['body'][tuple(some_type_combination)] = case_func

    def exec_func(*args, **kwargs):
        types_of_args = tuple(type(arg) for arg in args)
        if types_of_args in func_spec['domain']:
            return func_spec['body'][types_of_args](*args, **kwargs)
        else:
            return func_spec['std'](*args, **kwargs)

    func_spec['exec'] = exec_func
    globals()[name] = create_executable_function(name)

def spec_(name):
    for func in FUNCS_:
        if func['name'] == name:
            return func
    raise ValueError(f"Function specification for '{name}' not found.")

def std_(name):
    return spec_(name).get('std')

def domain_(name):
    return spec_(name).get('domain')

def body_(name):
    return spec_(name).get('body')

def exec_(name):
    return spec_(name).get('exec')

def update(name, part):
    spec = spec_(name)


new_(list, 'type with lists: mutable ordered tuples')

print(TYPES_)

init_('SUM', lambda *args: "Error")
print(FUNCS_)

new_(int, 'integers')

extend_('SUM', (int, int), lambda x,y: x+y)
print(FUNCS_)

print(SUM(2, 3))
print(SUM(2, 3.2))
