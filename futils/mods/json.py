from futils.core import op as op
from futils.core import logs as logs
from futils.core import iter as iter
from futils.core import comp as comp
from futils.mods import re as R
import json
import shlex
import ast

def is_(json_data):
    if json.loads(json_data):
        return True
i = is_

def echo(json_data, tab=4):
    print(json.dumps(json_data, indent=tab))
e = echo

def loads(json_data):
    return json.loads(json_data)
l = loads

def dumps(json_data):
    return json.dumps(json_data, indent=4)
d = dumps

def read(json_file):
    with n(json_file, 'r', encoding='utf-8') as jf:
        json_data = json.load(jf)
    return json_data
r = read

def write(output_json, json_data):
    with n(output_json, 'w', encoding='utf-8') as jf:
        json.dump(json_data, jf, indent=4)
w = write

def intersection(json_data_1, json_data_2):
    result = {}
    for key in json_data_1:
        if key in json_data_2:
            if op.bl(json_data_1[key], dict) and op.bl(json_data_2[key], dict):
                sub_result = intersection(json_data_1[key], json_data_2[key])
                if sub_result:
                    result[key] = sub_result
            elif op.eq(json_data_1[key], json_data_2[key]):
                result[key] = json_data_1[key]
            elif op.bl(json_data_1[key], list) and op.bl(json_data_2[key], list):
                sub_result = list(set(json_data_1[key]).intersection(json_data_2[key]))
                if sub_result:
                    result[key] = sub_result
    return result
cap = intersection

def union(json_data_1, json_data_2):
    result = json_data_1.c()
    for key, value in iter.items(json_data_2):
        if key not in result:
            result[key] = value
        else:
            if op.bl(result[key], dict) and op.bl(value, dict):
                result[key] = union(result[key], value)
            elif op.bl(result[key], list) and op.bl(value, list):
                result[key] = list(set(result[key] + value))
            elif result[key] != value:
                result[key] = value
    return result
cup = union

def remove(json_data, json_sub_data):
    if not json_sub_data:
        return json_data
    for key in json_sub_data:
        if key in json_data:
            del json_data[key]
    return json_data
rm = remove

def grep_keys(json_data, search_string='', case_sensitive=True):
    def match(string, substring, case_sensitive):
        if case_sensitive:
            return substring in string
        else:
            return op.lw(substring) in op.lw(string)
    if op.nl(search_string):
        return op.gk(json_data)
    else:
        keys_accumulator = {}
        if op.bl(json_data, dict):
            for key, value in json_data.items():
                if match(key, search_string, case_sensitive):
                    keys_accumulator[key] = value
                if op.bl(value, dict):
                    nested_keys = grep_keys(value, search_string, case_sensitive)
                    if nested_keys:
                        keys_accumulator[key] = nested_keys
                elif op.bl(value, list):
                    nested_keys_list = [grep_keys(item, search_string, case_sensitive) for item in value if op.bl(item, dict)]
                    nested_keys_list = [nk for nk in nested_keys_list if nk]
                    if nested_keys_list:
                        keys_accumulator[key] = nested_keys_list
        return keys_accumulator
grep_k = grep_keys
g_k = grep_k
gk = g_k

def grep_values(json_data, search_string, case_sensitive=True):
    def match(string, substring, case_sensitive):
        if case_sensitive:
            return substring in string
        else:
            return op.lw(substring) in op.lw(string)
    values_accumulator = {}
    if bl(json_data, dict):
        for key, value in json_data.items():
            if op.bl(value, dict):
                nested_values = grep_values(value, search_string, case_sensitive)
                if nested_values:
                    values_accumulator[key] = nested_values
            elif op.bl(value, list):
                matching_values = [item for item in value if match(str(item), search_string, case_sensitive)]
                if matching_values:
                    values_accumulator[key] = matching_values
            elif match(str(value), search_string):
                values_accumulator[key] = value
    return values_accumulator
grep_v = grep_values
g_v = grep_v
gv = g_v

def query(json_data, entry):
    keys = entry.split('.')
    value = json_data
    for key in keys:
        value = value[key]
    return value
jq = query
q = query

def grep(json_data, search_string, case_sensitive=True):
    def match(string, substring, case_sensitive):
        if case_sensitive:
            return substring in string
        else:
            return op.lw(substring) in op.lw(string)

    def parse_search_string(search_string):
        stack = []
        current_segment = []
        tokens = shlex.split(search_string)
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if op.eq(token, "("):
                iter.add(stack, current_segment)
                current_segment = []
            elif op.eq(token, ")"):
                expression = current_segment
                current_segment = stack.p
                iter.add(expression, current_segment)
            elif token.upper() in ("AND", "OR", "NOT"):
                iter.add(token.upper(), current_segment)
            elif op.eq(token.upper(), "WHERE"):
                if (i + 1) < len(tokens) and tokens[i + 1].upper() not in ("AND", "OR", "NOT", "(", ")"):
                    prev_token = current_segment.p
                    where_term = tokens[i + 1]
                    iter.add((prev_token, where_term), current_segment)
                    i += 1
            else:
                iter.add(token, current_segment)
            i += 1
        return current_segment
    def process_expression(json_content, expression_segment):
        if op.bl(expression_segment, tuple):
            subexpr, subwhere = expression_segment
            return process_search(json_content, subexpr.strip(), subwhere.strip())
        elif op.bl(expression_segment, list):
            result = process_expression(json_content, expression_segment[0])
            i = 1
            while op.lt(i, len(expression_segment)):
                if expression_segment[i] in ("AND", "OR"):
                    rator = expression_segment[i]
                    next_result = process_expression(json_content, expression_segment[i + 1])
                    result = combine_results(result, next_result, rator)
                    i += 1
                elif eq(expression_segment[i], "NOT"):
                    next_result = process_expression(json_content, expression_segment[i + 1])
                    result = remove(result, next_result)
                    i += 1
                i += 1
            return result
        else:
            return process_search(json_content, expression_segment.strip(), "key AND value")

    def process_search(json_content, search_term, where):
        search_term = search_term.strip()
        where = where.strip()
        if op.eq(where, "key"):
            return grep_k(json_content, search_term, case_sensitive)
        elif op.eq(where, "value"):
            return grep_v(json_content, search_term, case_sensitive)
        elif op.eq(where, "key AND value") or op.eq(where, "value AND key"):
            result = {}
            if op.bl(json_content, dict):
                for k, v in json_content.items():
                    match_key = match(k, search_term, case_sensitive)
                    match_value = match(str(v), search_term, case_sensitive) if op.n(bl)(v, dict) else False
                    if match_key and match_value:
                        result[k] = v
                    elif op.bl(v, dict):
                        nested_result = process_search(v, search_term, where)
                        if nested_result:
                            result[k] = nested_result
            return result
        elif where == "key OR value" or where == "value OR key":
            keys_result = grep_k(json_content, search_term, case_sensitive)
            values_result = grep_v(json_content, search_term, case_sensitive)
            return {**keys_result, **values_result}
        else:
            logs.err("The entry 'WHERE' must be 'key', 'value', 'key AND value', 'value AND key', 'key OR value', or 'value OR key'.")

    def combine_results(result1, result2, rator):
        if rator == "AND":
            return cap(result1, result2)
        elif rator == "OR":
            return cup(result1, result2)
        else:
            logs.err("rator must be 'AND' or 'OR'.")

    segments = parse_search_string(search_string)
    final_result = process_expression(json_data, segments)
    return final_result
g = grep

def sort(data):
    if op.bl(data, dict):
        return {k: sort(v) for k, v in sorted(data.items())}
    elif op.bl(data, list):
        sorted_list = [sort(elem) for elem in data]
    else:
        return data
s = sort

def to_json(key_value_string, remove=None):
    if op.bl(remove, int):
        segment = key_value_string.strip()[remove:-1].strip()
    else:
        segment = key_value_string.strip()

    pairs = R.f(segment, r"(\w+)=('[^']*'|\[[^\]]*\]|[^\s,]+)")
    segment_dict = {}
    for key, value in pairs:
        try:
            segment_dict[key] = ast.literal_eval(value)
        except:
            segment_dict[key] = value.strip("'")
    return segment_dict
