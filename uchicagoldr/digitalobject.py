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
        
    def add_object_part(self, file_object, config_data):
        assert isinstance(file_object, Item)
        self.representations.append(Representation(file_object))

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
        print(file_matching_parts)
        page_part_label = config_data.get('Object', 'page_part_label')
        page_part_group_position = config_data.get('Object', page_part_label)
        page_part = file_matching_parts[int(page_part_group_position)]
        page_number = file_matching_parts[ \
                            int(config_data.get('Object',
                                                config_data. \
                                                get('Object',
                                                    'number_label')))]. \
                                                    lstrip('0')
        current = None
        for n in self.pages:
            if n.page_number == page_number:
                current = n
                break
            else:
                pass

        if not current:
            page = Page(config_data)
            page.set_page_number(int(page_number))
            self.pages.append(page)
        else:
            page = current
        if not page.find_page_part(page_part):
            page.add_page_part(file_object, page_part)
            
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
