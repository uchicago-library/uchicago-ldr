from uchicagoldr.filepointer import FilePointer
from uchicagoldr.keyvaluepair import KeyValuePair


class Family(object):

    children = None
    descs = None

    def __init__(self, children=[], descs=[]):
        for child in children:
            assert(isinstance(child, Family) or
                   isinstance(child, FilePointer)
                   )
        for desc in descs:
            assert(isinstance(desc, KeyValuePair))
        self.children = children
        self.descs = descs

    def __repr__(self):
        return "Children: {}\nDescs: {}".format(
                                                str(self.children),
                                                str(self.descs)
                                               )

    def __hash__(self):
        objHash = 0
        for child in self.children:
            objHash = objHash ^ hash(child)
        for desc in self.descs:
            objHash = objHash ^ hash(desc)
        return objHash

    def __eq__(self, other):
        return (isinstance(other, Family) and
                hash(self) == hash(other))

    def __iter__(self):
        for child in self.children:
            yield child

    def _remove_desc_by_key(self, key_to_del):
        returns = []
        for desc in self.descs:
            if desc.get_key() == key_to_del:
                returns.append(self.descs.pop(self.descs.index(desc)))
        return returns

    def _remove_desc_by_value(self, value_to_del):
        returns = []
        for desc in self.descs:
            if desc.get_value() == value_to_del:
                returns.append(self.descs.pop(self.descs.index(desc)))
        return returns

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
        assert(not (child and index))
        if child is not None:
            try:
                return self.children.pop(self.children.index(child))
            except ValueError:
                return None
        if index is not None:
            try:
                return self.children.pop(index)
            except ValueError:
                return None

    def set_children(self, new_children):
        assert(isinstance(new_children, list))
        self.children = new_children

    def get_children(self):
        return self.children

    def get_child(self, child=None, index=None):
        assert(child is not None or index is not None)
        assert(not (child and index))
        if child is not None:
            try:
                return self.children[self.children.index(child)]
            except ValueError:
                return None
        if index is not None:
            try:
                return self.children[index]
            except ValueError:
                return None

    def add_desc(self, keyValuePair, index=None):
        assert(isinstance(keyValuePair, KeyValuePair))
        assert(keyValuePair not in self.descs)
        if index is None:
            self.descs.append(keyValuePair)
        else:
            assert(isinstance(index, int))
            assert(index > -1 and index < len(self.descs))
            self.descs.insert(index, keyValuePair)

    def remove_desc(self, key_to_del=None, value_to_del=None, index=None):
        returns = []
        if key_to_del is not None:
            returns.append(self._remove_desc_by_key(key_to_del))
        if value_to_del is not None:
            returns.append(self._remove_desc_by_value(value_to_del))
        if index is not None:
            try:
                assert(isinstance(index, int))
                returns.append(self.descs.pop(index))
            except:
                pass
        return returns

    def set_descs(self, new_descs):
        assert(isinstance(new_descs, list))
        for entry in new_descs:
            assert(isinstance(entry, KeyValuePair))
        self.descs = new_descs

    def get_descs(self):
        return self.descs

    def get_desc(self, key):
        for desc in self.descs:
            if desc.get_key() == key:
                return desc
