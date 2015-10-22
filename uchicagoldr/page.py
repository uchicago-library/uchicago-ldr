from uchicagoldr.item import Item

class Page_Part(object):
    def __init__(self, item, part_type):
        assert isinstance(item, Item)
        assert isinstance(part_type, str)
        self.part_type = part_type
        self.item = item
    
class Page(object):
    page_number = 0
    page_parts = []
    
    def __init__(self, page_number):
        self.page_number = page_number
        self.page_parts = []

    def find_page_part(self, page_type):
        is_this_part_available = [x for x in self.page_parts \
                                  if x.part_type == page_type]
        if len(is_this_part_available) > 0:
            return is_this_part_available[0]
        else:
            return None
        
    def get_page_number(self):
        return self.page_number

    def add_page_part(self, item, part_type):
        assert isinstance(item, Item)
        assert(part_type, str)
        check = self.find_page_part(part_type)
        new_part = Page_Part(item, part_type)
        self.page_parts.append(new_part)

