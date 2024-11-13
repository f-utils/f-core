import subprocess
from futils.core import *

def run(command, **kargs):
    command_list = command.format_map({**globals(), **locals(), **kargs}).split()
    process = subprocess.run(command_list, capture_output=True, text=True)
    return process.stderr, process.stdout

def which(command):
    return run(f'which {command}')

def ls(dir):
    return run(f'which {command}')
