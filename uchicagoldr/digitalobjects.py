
from uchicagoldr.item import Item

class DigitalObject(object):
    identifier = None
    page_parts = None
    object_parts = None

    def __init__(self, identifier):
        self.identifier = identifier
        self.page_parts = []
        self.object_parts = []

    def add_page(self, item):
        self.page_parts.append(item)

    def add_object_part(self, item):
        self.object_parts.append(item)
    
        
class DigitalObjects(object):
    objects = None
    object_pattern = None
    page_pattern = None
    
    def __init__(self, object_pattern, page_pattern):
        self.objects = []
        self.object_pattern = object_pattern
        self.page_pattern = page_pattern

    def add_object(self, item):
        assert isinstance(item, Item)
        item.match_object_pattern()

    
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
        
