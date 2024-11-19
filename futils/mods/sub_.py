import subprocess
import os

class SubErr(Exception):
    pass

def run(cmd, envs=None, **kargs):
    """
    inputs:
        cmd:
            type: str
            desc: the command to be executed
        envs:
            type: dict
            desc: dictionary with envs and its values to append the os envs
    outputs:
        stderr:
            type: str
            desc: the stderr of the executed command
        stdout:
            type: str
            desc: the stdout of the executed command
    raises:
    aliases:
    """
    cmd_list = cmd.format_map({**globals(), **locals(), **kargs}).split()
    env = os.environ.copy()
    if envs:
        env.update(envs)
    process = subprocess.run(cmd_list, capture_output=True, text=True, env=env)
    return process.stderr, process.stdout

def which(cmd):
    return run(f'which {cmd}')

def ls(path):
    return run(f'ls {path}')

def la(path):
    return run(f'ls -a {path}')
