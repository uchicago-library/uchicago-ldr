
from configparser import ConfigParser
from itertools import combinations
from re import compile as re_compile, split as re_split

class DigitalObject(object):
    object_identifier = ""
    object_files = []

    def __init__(self, identifier):
        self.object_identifier = identifier
        self.object_files = []

    def add_file(self, file_object):
        self.object_files.append(file_object)

    def find_object_identifier(self, control_type_data):
        object_pattern = control_type_data.get('object')
        assert object_pattern
        pattern_search = re_compile(object_pattern).search(self.filepath)
        if pattern_search:
            return namedtuple("data", "valid keys")( \
                                                     True,
                                                     pattern_search.groups() \
            )
        else:
            return namedtuple("data", "valid keys")( \
                                                     False,
                                                     None \
            )

    def validate_filename(self, filepath, object_map, identifier_groups):
        assert isinstance(filepath, str)
        assert isinstance(object_map, ConfigParser)
        assert isinstance(identifier_groups, tuple)
        header = re_compile('^\d{4}-\d{3}/')
        check_for_scrc_header = header.search(filepath)
        if header.search(filepath):
            header, adjusted_filepath = re_split(header,filepath)
            filepath_items = re_split('/|-|_',
                                      adjusted_filepath \
                                      [:adjusted_filepath.find('.')])
        else:
            filepath_items = re_splite('/|_|-',filepath)
        for label in object_map.get('Object', 'labels').split(','):
            label_positions = object_map.get('Object', label)
            if label_positions.find(',') != -1:
                label_positions = [int(x) \
                                   for x in label_positions.split(',')]
            else:
                label_positions = [int(label_positions)]
            if False in [filepath_items[x] == \
                         filepath_items[y] \
                         for x,y in combinations(label_positions,2)]:
                return False
        return True
        
    def get_identifier(self):
        return self.object_identifier
    
    def classify_file_type(self, control_type_data):
        page_pattern = control_type_data.get('page_file')
        object_pattern = control_type_data.get('object_file')
        page_pattern_search = re_compile(page_pattern).search(self.filepath)
        object_pattern_search = re_compile(object_pattern). \
                                search(self.filepath)
        pagenumber = None
        if page_pattern_search:
            groups = page_pattern_search.groups()
            pagenumber = groups[-2]
            pagenumber = pagenumber.lstrip('0')
            tag = "page_file"
        elif object_pattern:
            tag = "object_file"
        else:
            tag = "undefinable"
        self.tag = tag
        if pagenumber:
            self.pagenumber = pagenumber
