from re import compile as re_compile, split as re_split

from uchicagoldr.item import Item
from configparser import ConfigParser

class Page_Part(Item):
    
    def __init__(self, item, config_data):
        self.item = item

        
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
    object_files = []
    page_files = []
    
    def __init__(self, identifier):
        self.identifier = identifier
        self.object_files = []
        self.page_files = []
        
    def add_object_file(self, file_object):
        self.object_files.append(file_object)

    def add_page_file(self, file_object):
        self.page_files.append(file_object)        
        
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
