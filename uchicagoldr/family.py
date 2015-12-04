from uchicagoldr.filepointer import FilePointer


class Family(object):

    children = None
    descs = None
    locked = False

    def __init__(self, children=[], descs={}):
        for child in children:
            assert(isinstance(child, Family) or
                   isinstance(child, FilePointer)
                   )
        assert(self._test_limited_dict_values(descs))
        self.children = children
        self.descs = descs

    def __hash__(self):
        assert(self.locked)
        objHash = 0
        for child in self.children:
            objHash = hash(objHash ^ hash(child))

    def __eq__(self, other):
        return (isinstance(other, Family) and
                hash(self) == hash(other))

    def _test_limited_dict_values(self, dictionary):
        limited = True
        for entry in dictionary:
            value = dictionary[entry]
            if not isinstance(value, str) and  \
                    not isinstance(value, int) and \
                    not isinstance(value, None):
                return False
            if isinstance(value, dict):
                limited = limited and self._limit_dict_values(value)
                if limited is False:
                    return False
        return limited

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def __lock_children(self):
        pass

    def __unlock_children(self):
        pass

    def __lock_descs(self):
        pass

    def __unlock_descs(self):
        pass

    def add_child(self, child, index=None):
        assert(isinstance(child, Family) or
               isinstance(child, FilePointer))
        assert(child not in self.children)

        if index is None:
            self.children.append(child)
        else:
            assert(isinstance(index, int))
            assert(index > -1 and index < len(self.children))
            self.children.insert(index, child)

    def remove_child(self, child=None, index=None):
        assert(child is not None or index is not None)
        if child is not None:
            try:
                return self.children.pop(index(child))
            except ValueError:
                return None
        if index is not None:
            try:
                return self.children.pop(index)
            except ValueError:
                return None

    def set_children(self, new_children):
        pass

    def get_children(self):
        return self.children

    def add_desc(self, key, value):
        pass

    def remove_desc(self, key):
        pass

    def set_descs(self, new_desc):
        pass

    def get_descs(self):
        return self.desc
