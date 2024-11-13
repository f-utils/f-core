from futils.core import op as op
from futils.core import logs as logs
from futils.core import hash as hash
from futils.mods import path as P
from futils.mods import json as J
import base64
import json
import requests

class HttpErr(Exception):
    pass

def encode_basic(user_pass):
        user_pass_str = f"{user_pass[0]}:{user_pass[1]}"
        encoded = base64.b64encode(user_pass_str.encode('utf-8')).decode('utf-8')
        return {'Authorization': f'Basic {encoded}'}

def auth(key, kind='bearer'):
    if op.eq(kind, bearer) or op.eq(op.lw(kind), 'bearer'):
        'Authorization: Bearer {key}'
    elif op.eq(kind, basic) or op.eq(op.lw(kind), 'basic'):
        if op.bl(key, str):
            if hash.is_encoded(key):
                return {'Authorization': f'Basic {key}'}
            else:
                logs.err(f'The string {key} is not a base64 encoded string.')
        elif op.bl(key, (list, tuple, set)):
            if op.eq(len(key), 2):
                return encode_basic(key)
            else:
                logs.err('Provided list, tuple, or set must contain exactly two elements.')
        elif op.bl(key, dict):
            if op.eq(len(key), 2):
                user_pass = next(iter(items(key)))
                return encode_basic(user_pass)
            else:
                logs.err('Provided dictionary must contain exactly two keys.')
        else:
            logs.err('Invalid key type for Basic authentication.')
    elif op.eq(kind, api) or op.eq(op.lw(kind), 'api'):
        return {'Authorization': f'API {key}'}
    else:
        logs.err('Unsupported authentication type specified.')

def mime(content_type):
    return {'Content-Type': content_type}

def agent(user_agent):
    return {'User-Agent': user_agent}

def get(url, headers={}, data='', params={}, output_file_path='', wb=False):
    try:
        response = requests.get(url, headers=headers, data=data)
        if response.status_code == 200:
            if output_file_path:
                if wb:
                    P.wb(output_file_path, response.content)
                else:
                    try:
                        J.w(output_file_path, json.loads(response.content))
                    except:
                        P.w(output_file_path, response.content)
            else:
                return response.content
        else:
            return response.status_code, response.reason
    except requests.exceptions.RequestException as e:
            logs.err(f'Request failed: {e}')

def post(url, headers='', data=''):
    try:
        response = requests.get(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.content
        else:
            return response.status_code, response.reason
    except requests.exceptions.RequestException as e:
            logs.err(f'Request failed: {e}')

