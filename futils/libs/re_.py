from futils.core.op import *
from futils.core.iter import *
from futils.mods import path_ as P
import re

class ReErr(Exception):
    pass

def is_(regex):
    if re.compile(regex):
        return re.compile(regex)
i = is_

def match(string, regex, full=True):
    regex = i(regex)
    if full:
        if re.fullmatch(regex, str(string)):
            return True
        return False
    if re.match(regex, str(string)):
        return True
    return False
m = match

def grep(string, regex, group=0):
    match = re.search(regex, str(string))
    if match:
        return match.group(group)
g = grep

def find(string, regex):
    return re.findall(regex, string)
f = find

def begins(string, regex):
    regex = r'^' + regex
    if ne(grep(string, regex), None):
        return True
    return False
b = begins

def ends(string, regex):
    regex = regex + r'$'
    if ne(grep(regex, string), None):
        return True
    return False
e = ends

def get_lines(regex, file_path):
    matched_lines = []
    content_lines = P.gl(file_path)
    for line in content_lines:
        if grep(line, regex):
            add(line, matched_lines)
    return matched_lines
gl = get_lines

def between_lines(regex_start, regex_end, file_path):
    content_between_lines = []
    capture = False
    content_lines = P.gl(file_path)
    for line in content_lines:
        if grep(line, regex_start):
            capture = True
            continue
        if grep(line, regex_end):
            break
        if capture:
            add(line, content_between_lines)
    return to_str(content_between_lines, "\n")
b_lines = between_lines
b_l = b_lines
bl = b_l
