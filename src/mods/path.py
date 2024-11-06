from . import op
from . import logs
import os
import sys
from pathlib import Path
import inspect
import fnmatch
import shutil

def rel():
    pass

def abs():
    pass

def resolve(x):
    return Path(x).resolve()
rsl = resolve

def is_abs(x):
    return resolve(x).is_absolute()
is_a = is_abs
isa = is_a

def is_rel(x):
    return op.n(is_abs)(x)
is_r = is_rel
isrel = is_rel
isr = is_r

def file():
    pass
f = file

def dir():
    pass
d = dir

def is_file(x):
    return os.path.isfile(x)
is_f = is_file
isf = is_f

def is_dir(x):
    return os.path.isdir(x)
is_d = is_dir
isd = is_d

def is_(x, kind):
    if (op.eq(kind, a) or op.eq(kind, 'abs')) and isa(x):
        return True
    elif (op.eq(kind, r) or op.eq(kind, 'rel')) and isr(x):
        return True
    elif (op.eq(kind, f) or op.eq(kind, 'file')) and isf(x):
            return True
    elif (op.eq(kind, d) or op.eq(kind, 'dir')) and isd(x):
            return True
    else:
        logs.err('The kind must be abs/rel/file/dir.')
i = is_

def read(x, encoding='utf-8'):
    with open(x, 'r', encoding=encoding) as f:
        content = f.read()
    return content
r = read

def read_binary(x):
    with open(x, 'rb') as f:
        content = f.read()
    return content
r_binary = read_binary
rb = read_binary

def write(x, content='', encoding='utf-8', overwrite=True):
    if isf(x) and overwrite:
        with open(x, 'w', encoding=encoding) as f:
            f.write(content)
    else:
        with open(x, 'w', encoding=encoding) as f:
            f.write(content)
w = write

def write_binary(x, content='', overwrite=True):
    if is_f(x) and overwrite:
        with open(x, 'wb') as f:
            f.write(content)
    else:
        with open(x, 'wb') as f:
            f.write(content)
w_binary = write_binary
wb = w_binary

def lines(file):
    content = r(file)
    return content.splitlines()
l = lines

def basename(x):
    return rsl(x).name
base_name = basename
b_n  = base_name
bn = b_n

def filename(x):
    name, _ = os.path.splitext(bn(x))
    return name
file_name = filename
f_n  = file_name
fn = f_n

def extension(x):
    _, ext = os.path.splitext(bn(x))
    return ext
ext = extension

def dirname(x):
    return rsl(x).parent
dir_name = dirname
d_n = dir_name
dn = d_n

def name(x, kind):
    if op.eq(kind, d) or op.eq(kind, 'dir'):
        dn(x)
    elif op.eq(kind, f) or op.eq(kind, 'file'):
        fn(x)
    else:
        logs.err('The kind must be dir/file.')
n = name

def split(x):
    return Path(x).parts
s = split

def union(*args):
    return os.path.abspath(os.path.join(*args))
cup = union

def parent(x, N=1):
    for _ in range(N):
        path = Path(x).parent
    return path
p = parent

def here(path):
    caller_frame = inspect.stack()[1]
    caller_filepath = caller_frame.filename
    script_dir = Path(caller_filepath).resolve().parent
    return cup(script_dir, path)
h = here

def lt(x, y):
    path = resolve(y)
    sub_path = Path(x)

    sub_path_str = str(Path('/') / sub_path)
    path_str = str(path)
    if path_str.find(sub_path_str) != -1:
        return True
    return False
sub = lt

def mkdir(path):
    os.makedirs(path, exist_ok=True)
make_dir = mkdir
mk_d = make_dir
mkd = mk_d

def touch(x):
    mkd(nd(x))
    w(x)
make_file = touch
mk_f = make_file
mkf = mk_f

def make(x, kind):
    if op.eq(kind, d) or op.eq(kind, 'dir'):
        mkd(x)
    elif op.eq(kind, f) or op.eq(kind, 'file'):
        mkf(x)
    else:
        logs.err('The kind must be file/dir.')
mk = make

def list_files(x):
    files = []
    for f in os.listdir(x):
        if isf(cup(x, f)):
            files += [cup(x, f)]
    return files
ls_files = list_files
lsf = ls_files

def list_dirs(x):
    dirs = []
    for d in os.listdir(x):
        if isd(cup(x, d)):
            dirs += [cup(x, d)]
    return dirs
ls_dirs = list_dirs
lsd = ls_dirs

def ls(x, kind=None):
    if op.eq(kind, None):
        return [f for f in os.listdir(x)]
    elif op.eq(kind, d) or op.eq(kind, 'dir'):
        return lsd(x)
    elif op.eq(kind, f) or op.eq(kind, 'file'):
        return lsf(x)
    else:
        logs.err('kind must be empty, file or dir')

def find(path, regex, kind=None, mindepth=0, maxdepth=float('inf')):
    matches = {"files": [], "dirs": []} if kind is None else []
    for root, dirnames, filenames in os.walk(path):
        depth = root[len(path):].count(os.sep)
        if op.lt(depth, mindepth):
            continue
        if op.gt(depth, maxdepth):
            dirnames[:] = []
            continue
        if op.bl(kind, [f, 'file', None]):
            for filename in fnmatch.filter(filenames, pattern):
                path = cup(root, filename)
                if op.eq(kind, f) or  op.eq(kind, 'file'):
                    matches.append(path)
                else:
                    matches["files"].append(path)
        if op.bl(kind, [d, 'dir', None]):
            for dirname in fnmatch.filter(dirnames, pattern):
                path = cup(root, dirname)
                if kind == Path.d:
                    matches.append(path)
                else:
                    matches["dirs"].append(path)
        if  op.nb(kind, [None, Path.f, Path.d]):
            logs.err("Invalid kind. Use Path.file, Path.dir, or None.")
    return matches

def copy_file(input_path, output_path):
    if isf(input_path):
        if isd(output_path):
            file_name = bn(input_path)
            shutil.copy2(input_path, cup(output_path, file_name))
        shutil.copy2(input_path, output_path)
    else:
        logs.err(f'The file {input_path} does not exists.')
cp_file = copy_file
cp_f = cp_file
cpf = cp_f

def copy_dir(input_path, output_path):
    if isd(input_path):
        if not os.path.exists(destination_directory):
            shutil.copytree(input_path, output_path)
        logs.err(f'The path {output_path} already exists')
    logs.err(f'The dir {input_path} does not exists.')
cp_dir = copy_dir
cp_d = cp_dir
cpd = cp_d

def copy(input_path, output_path):
    if isf(input_path):
        cpf(input_path, output_path)
    elif isd(input_path):
        cpd(input_path, output_path)
    else:
        logs.err(f'{input_path} does not exists.')
cp = copy
