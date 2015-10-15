
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
