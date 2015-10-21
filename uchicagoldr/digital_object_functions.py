
from os.path import isabs
from re import compile as re_compile, split as re_split

def validate_filename(filepath, pattern):
    def find_pattern_in_a_string():
        pat = re_compile(pattern)
        if not pattern.search(filepath):
            return None
        return pattern

    pattern = re_compile(pattern)
    if not pattern.search(filepath):
        return False
    return re_split('^\d{4}-\d{3}', filepath)

def split_filepath_into_list_of_words(filepath):
    if isabs(filepath):
        filepath = filepath[1:]
    if not filepath.find('.') == -1:
        filepath = filepath[:filepath.find('.')]
    c = re_split('/|-|_', filepath)
    return c

def construct_identifier(identifier_parts, identifier_values):
    identifier = []
    for n in identifier_parts:
        identifier.append(identifier_values[n])
    return '-'.join(identifier)

def does_object_exist(identifier, list_of_objects):
    for n in list_of_objects:
        if n.get_identifier() == identifier:
            return n
    return None

def get_truthiness_of_list(a_list):
    o = True
    for n in a_list:
       o = o&n
       if not o:
           break
    return 0

def is_string_a_list(a_string):
    return a_string.find(',')

def transform_comma_string_into_list(a_string):
    return a_string.split(',')

def validate_filename_id_placement(filename_parts, id_parts):
    for id_nums in id_parts:
        if is_string_a_list(id_nums):
            string_into_list = transform_comma_string_into_list(id_nums)
            n_items = [int(x) for x in string_into_list]
            prev = None
            for t in n_items:
                if prev:
                    if prev == filename[t]:
                        prev = filename[t]
                    else:
                        return False
        else:
            pass
    return True
