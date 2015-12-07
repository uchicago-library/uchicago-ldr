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

    def __repr__(self):
        return "Locked: {}\nChildren: {}\nDescs: {}".format(
                                                str(self.locked),
                                                str(self.children),
                                                str(self.descs))

    def __hash__(self):
        assert(self.locked)
        objHash = 0
        for child in self.children:
            objHash = hash(objHash ^ hash(child))
        for k, v in self.descs:
            addHash = hash(k)+hash(v)
            objHash = hash(objHash ^ addHash)
        return objHash

    def __eq__(self, other):
        return (isinstance(other, Family) and
                hash(self) == hash(other))

    def __iter__(self):
        for child in self.children:
            yield child

    def _test_limited_dict_values(self, dictionary):
        limited = True
        for key, value in dictionary.items():
            if not isinstance(key, str):
                return False
            if not isinstance(value, str) and  \
                    not isinstance(value, int) and \
                    not isinstance(value, dict) and \
                    value is not None:
                return False
            if isinstance(value, dict):
                limited = limited and self._test_limited_dict_values(value)
                if limited is False:
                    return False
        return limited

    def _dict_to_nested_tuples(self, dictionary):
        tuplesList = []
        sortedKeys = sorted(dictionary)

        for key in sortedKeys:
            value = dictionary[key]
            if isinstance(value, dict):
                tuplesList.append((key, self._dict_to_nested_tuples(value)))
            else:
                tuplesList.append((key, value))
        return tuple(tuplesList)

    def _nested_tuples_to_dict(self, tuples):
        dictionary = {}
        for entry in tuples:
            key, value = entry
            assert(isinstance(key, str))
            if isinstance(value, tuple):
                dictionary[key] = self._nested_tuples_to_dict(value)
            else:
                assert(
                    isinstance(value, str) or
                    isinstance(value, int) or
                    value is None
                )
                dictionary[key] = value
        return dictionary

    def lock(self):
        assert(not self.locked)
        try:
            self.children = tuple(self.children)
            self.descs = self._dict_to_nested_tuples(self.descs)
            self.locked = True
            return True
        except:
            return False

    def unlock(self):
        assert(self.locked)
        try:
            self.children = list(self.children)
            self.descs = self._nested_tuples_to_dict(self.descs)
            self.locked = False
            return True
        except:
            return False

    def add_child(self, child, index=None):
        assert(not self.locked)
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
        assert(not self.locked)
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
        assert(not self.locked)
        assert(isinstance(new_children, list))
        self.children = new_children

    def get_children(self):
        return self.children

    def add_desc(self, key, value):
        assert(not self.locked)
        assert(isinstance(key, str))
        if isinstance(value, dict):
            assert(self._test_limited_limited_dict_values(value))
            self.descs[key] = value
        else:
            assert(
                isinstance(value, str) or
                isinstance(value, int) or
                isinstance(value, None)
            )
            self.descs[key] = value

    def remove_desc(self, key_to_del):
        assert(not self.locked)
        self.descs = {key: value for key, value in self.desc.items()
                      if key != key_to_del}

    def set_descs(self, new_descs):
        assert(not self.locked)
        assert(self._test_limited_dict_values(new_descs))
        self.descs = new_descs

    def get_descs(self):
        return self.desc
