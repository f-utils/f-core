from futils.core.logs import *
from futils.core.op import *
import hashlib
import time
import base64

def include(entry):
    if bl(entry, int):
        sys.path.append(os.path.abspath(__file__ + '/../' * entry))
    elif bl(entry, str):
        if os.path.exists(entry):
            sys.path.append(entry)
        else:
            err(f"The provided path does not exist.")
    else:
        err("Input must be either an integer or a valid path.")

def load(env_path='.env'):
    try:
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, sep, value = line.partition('=')
                if sep == '=':
                    os.environ[key.strip()] = value.strip()
    except:
        err(f"{file_path} not found.")

def env(env_var):
    return os.getenv(env_var)

def random(size):
    num_bytes = (size + 1) // 2
    random_bytes = os.urandom(num_bytes)
    hash_object = hashlib.sha256(random_bytes)
    hex_hash = hash_object.hexdigest()
    return hex_hash[:size]
rnd = random

def sleep(n):
    return time.sleep(n)

def kill(status):
    sys.kill(status)

def rse(ClssErr, message):
    raise ClssErr(message)

