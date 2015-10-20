from re import compile as re_compile, split as re_split

from uchicagoldr.item import Item
from configparser import ConfigParser
from re import compile as re_compile

class Page_Part(Item):
    def __init__(self, item, config_data):
        file_type = config_data.get('Object', 'file_type')
        pattern = config_data.get('Object', 'pattern')
        if item.has_header():
            filepath = item.canonical_filepath.split(item.get_header())[1]
        else:
            filepath = item.canonical_filepath
        print(re_compile(pattern).search(filepath).groups())
        self.item = item

class Object_Part(Item):
    def __init__(self, item, config_data):
        pattern = config_data.get('Object', 'pattern')
        if item.has_header():
            filepath = item.canonical_filepath.split(item.get_header())[1]
        else:
            filepath = item.canonical_filepath
        
        print(re_compile(pattern).search(item.canonical_filepath).groups())
        
class Page(object):
    page_parts = []
    page_number = 0

    def __init__(self):
        self.page_number = 0
        self.page_parts = []

    def set_page_number(self,number):
        assert isinstance(number,int)
        if self.page.number > 0:
            raise ValueError("can't set page number twice")
        else:
            self.page_number = number

    def get_page_number(self):
        return self.page_number
                
    def add_page_part(self,item,config_data):
        assert isinstance(item, Item)
        assert isinstance(config_data, ConfigParser)
        new_part = Page_Part(item)
        self.page_parts.append(new_part, config_data)
        
class DigitalObject(object):
    object_identifier = ""
    representations = []
    pages = []
    
    def __init__(self, identifier):
        self.identifier = identifier
        self.object_files = []
        self.page_files = []
        
    def add_object_part(self, file_object, config_data):
        assert isinstance(file_object, Item)
        Object_Part(file_object, config_data)
        self.object_files.append(file_object)

    def add_page(self, file_object, config_data):
        assert isinstance(file_object, Item)
        assert isinstance(config_data, ConfigParser)
        pattern = config_data.get('Object', 'pattern')
        if file_object.has_header():
            filepath = file_object.canonical_filepath. \
                       split(item.get_header())[1]
        else:
            filepath = file_object.canonical_filepath
            
        file_matching_parts = re_compile(pattern).search(filepath).groups()
        
        page_part_label = config_data.get('Object', 'page_part_label')
        
        file_part_labels = config_data.get('Object', 'labels').split(',')
        file_part_label_check = file_part_labels.index(page_part_label)
        if file_part_label_check != -1:
            page_part_index = config_data.get('Object', page_part_label)
            page_type = file_matching_parts \
                        [int(config_data.get('Object', page_part_label))]
            if not page_type in config_data.get('Object', 'parts'):
                return False
            page_number = file_matching_parts[int(config_data.get('Object', config_data.get('Object', 'number_label')))].lstrip('0')
            
        else:
            return False
        
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
        return self.identifier
    
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
