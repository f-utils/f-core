import inspect
import textwrap

TYPES_ = {}
FUNCS_ = {}

def _register_(type_name, description):
    if type_name in TYPES_:
        raise ValueError(f"Type '{type_name}' is already registered.")

    TYPES_[type_name] = description

def _init_(name, description, std_func):
    if name in FUNCS_:
        raise ValueError(f"Function '{name}' is already initialized.")

    func_structure = {
        'name': name,
        'description': description,
        'std': std_func,
        'body': {},
        'exec': None,
        'domain': [],
        'std_repr': _get_function_repr(std_func)
    }

    exec_func = _mk_exec_func_(name)
    globals()[name] = exec_func
    FUNCS_[exec_func] = func_structure

def _mk_exec_func_(name):
    def exec_func(*args, **kwargs):
        func_spec = _spec_(name)
        exec_func = func_spec['exec']
        if exec_func:
            return exec_func(*args, **kwargs)
        else:
            return func_spec['std'](*args, **kwargs)
    return exec_func

def _extend_(name, arg_and_kwarg_types, case_func):
    if not callable(case_func):
        raise ValueError("case_func must be callable.")

    if isinstance(arg_and_kwarg_types, dict):
        arg_types = ()
        kwarg_types = arg_and_kwarg_types
    elif isinstance(arg_and_kwarg_types, tuple):
        split_index = next((i for i, t in enumerate(arg_and_kwarg_types) if isinstance(t, dict)), len(arg_and_kwarg_types))
        arg_types = arg_and_kwarg_types[:split_index]
        kwarg_types = arg_and_kwarg_types[split_index] if split_index < len(arg_and_kwarg_types) else {}
    elif isinstance(arg_and_kwarg_types, type):
        arg_types = (arg_and_kwarg_types,)
        kwarg_types = {}
    else:
        raise ValueError("Invalid format for argument types. Must be a type, dict, or tuple.")

    if not all(t in TYPES_ for t in arg_types):
        raise ValueError("All positional argument types must be registered in TYPES_.")
    if not all(t in TYPES_ for t in kwarg_types.values()):
        raise ValueError("All keyword argument types must be registered in TYPES_.")

    func_spec = _spec_(name)

    if (tuple(arg_types), frozenset(kwarg_types.items())) in func_spec['body']:
        raise ValueError(f"The type combination '{arg_types}' with '{kwarg_types}' is already in domain for function '{name}'.")

    func_spec['body'][(tuple(arg_types), frozenset(kwarg_types.items()))] = {
        'func': case_func,
        'repr': _get_function_repr(case_func)
    }
    func_spec['domain'].append((arg_types, kwarg_types))

    def exec_func(*args, **kwargs):
        args_types = tuple(type(arg) for arg in args)
        kwargs_types = frozenset({key: type(kwargs[key]) for key in kwargs}.items())

        for (arg_combo, kwarg_combo), func_info in func_spec['body'].items():
            if args_types == arg_combo and kwargs_types <= kwarg_combo:
                return func_info['func'](*args, **kwargs)

        return func_spec['std'](*args, **kwargs)

    func_spec['exec'] = exec_func
    globals()[name] = _mk_exec_func_(name)
    FUNCS_[globals()[name]] = func_spec

def _get_function_repr(func):
    try:
        source = inspect.getsource(func).strip()
    except (OSError, TypeError):
        source = repr(func)

    if "lambda" in source:
        # Clean up the lambda representation
        lambda_idx = source.index("lambda")
        return source[lambda_idx:].strip().rstrip(')')
    return source

def _spec_(f):
    if callable(f) and f in FUNCS_:
        return FUNCS_[f]
    elif isinstance(f, str):
        func_object = globals().get(f)
        if func_object in FUNCS_:
            return FUNCS_[func_object]
    raise ValueError(f"Function specification for '{f}' not found.")

def _type_str_(type_tuple, kwarg_dict):
    arg_str = ', '.join(t.__name__ for t in type_tuple)
    kwarg_str = ', '.join(f"{key}: {t.__name__}" for key, t in kwarg_dict.items())
    return ', '.join(filter(None, [arg_str, kwarg_str]))

def _info_(f, what='spec'):
    spec = _spec_(f)
    if what == 'spec':
        wrapped_desc = textwrap.fill(f"{spec['description']}", width=84)
        print(f"Spectrum of function '{spec['name']}':")
        print("  DESC:")
        print(f"    {wrapped_desc}")
        print("  STD:")
        print(f"    {spec['std_repr']}")
        print("  DOMAIN:")
        for i, (arg_types, kwarg_types) in enumerate(spec['domain'], 1):
            print(f"    {i}. {_type_str_(arg_types, kwarg_types)}")
        print("  BODY:")
        for i, ((arg_combo, kwarg_combo), func_info) in enumerate(spec['body'].items(), 1):
            print(f"    {i}. {_type_str_(arg_combo, dict(kwarg_combo))} => {func_info['repr']}")
    elif what == 'domain':
        print(f"Domain of function '{spec['name']}':")
        for i, (arg_types, kwarg_types) in enumerate(spec['domain'], 1):
            print(f"    {i}. {_type_str_(arg_types, kwarg_types)}")
    elif what == 'std':
        print(f"Standard return for function '{spec['name']}':")
        print(f"    {spec['std_repr']}")
    elif what == 'body':
        print(f"Body of function '{spec['name']}':")
        for i, ((arg_combo, kwarg_combo), func_info) in enumerate(spec['body'].items(), 1):
            print(f"    {i}. {_type_str_(arg_combo, dict(kwarg_combo))} => {func_info['repr']}")
    elif what == 'desc':
        print(f"Description of function '{spec['name']}':")
        print(f"    {spec['description']}")
    else:
        raise ValueError(f"Unknown attribute '{what}' to print.")

def _update_(f, attribute):
    spec = _spec_(f)

    if attribute == 'desc':
        def update_description(new_description):
            spec['description'] = new_description
        return update_description

    if attribute == 'std':
        def update_standard(new_std_func):
            spec['std'] = new_std_func
            spec['std_repr'] = _get_function_repr(new_std_func)
            globals()[spec['name']] = _mk_exec_func_(spec['name'])
            FUNCS_[globals()[spec['name']]] = spec
        return update_standard

    if attribute == 'body':
        def update_body(type_argument, new_argument_function):
            if type_argument not in TYPES_:
                raise ValueError(f"Type '{type_argument}' not registered.")
            for (arg_types, kwarg_types), func in spec['body'].items():
                if type_argument in arg_types:
                    spec['body'][(arg_types, kwarg_types)] = {
                        'func': new_argument_function,
                        'repr': _get_function_repr(new_argument_function)
                    }
                    globals()[spec['name']] = _mk_exec_func_(spec['name'])
                    FUNCS_[globals()[spec['name']]] = spec
                    return
            raise ValueError(f"Type '{type_argument}' not found in domain.")
        return update_body

    raise ValueError(f"Unknown update attribute '{attribute}'.")

_register_(int,   'integers numbers')
_register_(float, 'float numbers')


