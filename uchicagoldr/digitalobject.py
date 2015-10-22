from configparser import ConfigParser
from re import compile as re_compile, split as re_split

from uchicagoldr.page import Page, Page_Part
from uchicagoldr.item import Item
from uchicagoldr.representation import Representation

class DigitalObject(object):
    object_identifier = ""
    representations = []
    pages = []
    
    def __init__(self, identifier):
        self.identifier = identifier
        self.representations = []
        self.pages = []
        
    def add_representation(self, file_object):
        assert isinstance(file_object, Item)
        if self.find_a_representation(file_object):
            None
        else:
            new = Representation(file_object)
            self.representations.append(new)
        return new
    
    def find_a_page(self, page_number):
        for n in self.pages:
            if n.page_number == page_number:
                return n
        return None


    def find_a_representation(self, other):
        assert isinstance(other, Item)
        for n in self.representations:
            if n.item.canonical_filepath == other.canonical_filepath:
                return n
        return None
    
    def add_page(self, file_object, page_num, part_type):
        assert isinstance(file_object, Item)
        assert isinstance(page_num, int)
        if self.find_a_page(page_num):
            page_obj = self.find_a_page(page_num)
        else:
            page_obj = Page(page_num)
            self.pages.append(page_obj)
        page_obj.add_page_part(file_object, part_type)
        return page_obj
          
    def get_pages(self):
        return self.pages

    def is_page_sequence_complete(self):
        last_page = max([x.page_number for x in self.pages])
        completed_sequence = [x for x in range(1,last_page)]
        missing = []
        for n in completed_sequence:
            if n in [x.page_number for x in self.pages]:
                pass
            else:
                missing.append(n)
        if len(missing) > 0:
            return missing
        return True

    def are_pages_complete(self, config_data):
        assert isinstance(config_data, ConfigParser)
        page_parts = config_data.get('Object', 'parts').split(',')
        incomplete = []
        for page in self.pages:
            this_page_parts = [x.part_type for x in page.page_parts]
            if set(page_parts) - set(this_page_parts) != set([]):
                incomplete.append(page)
        if len(incomplete) > 0:
            return incomplete
        return True
    
    def get_representations(self):
        return self.representations
    
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
