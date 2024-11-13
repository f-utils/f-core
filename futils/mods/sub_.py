import subprocess

class SubErr(Exception):
    pass

def run(command, **kargs):
    command_list = command.format_map({**globals(), **locals(), **kargs}).split()
    process = subprocess.run(command_list, capture_output=True, text=True)
    return process.stderr, process.stdout

def which(command):
    return run(f'which {command}')

def ls(path):
    return run(f'ls {command}')

def la(path):
    return run(f'ls -a {command}')
