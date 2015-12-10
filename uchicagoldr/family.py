from pickle import dump
from os import getcwd
from os.path import exists, isdir, join
from uuid import uuid4

from uchicagoldr.filepointer import FilePointer
from uchicagoldr.keyvaluepair import KeyValuePair
from uchicagoldr.keyvaluepairlist import KeyValuePairList


class Family(object):

    # For pickling... #.#.# = incompat.not_a_good_idea.minor_upgrade
    version = "0.0.1"

    def __init__(self, children=None, descs=None):

        self.children = []
        self.descs = []

        assert(isinstance(children, list) or children is None)
        assert(isinstance(descs, KeyValuePairList) or descs is None)
        if children is not None:
            for child in children:
                self.add_child(child)
        if descs is not None:
            for desc in descs:
                self.add_desc(desc)
        self.uuid = str(uuid4())

    def __repr__(self):
        return "UUID: {}\nChildren: {}\nDescs: {}".format(self.uuid,
                                                          str(self.children),
                                                          str(self.descs)
                                                          )

    def add_child(self, child, index=None):
        assert(isinstance(child, Family) or
               isinstance(child, FilePointer))
        for cur_child in self.get_children():
            assert(child is not cur_child)

        if index is None:
            self.children.append(child)
        else:
            assert(isinstance(index, int))
            assert(index > -1 and index < len(self.children))
            self.children.insert(index, child)

    def remove_child(self, child=None, index=None):
        assert(child is not None or index is not None)
        assert(bool(child) + bool(index) == 1)  # xor
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

    def __str__(self, depth=0):
        strRep = "UUID: {}\n".format(self.uuid)
        strRep = strRep+"\t"*depth+"Descs: "+str(len(self.get_descs()))
        for desc in self.get_descs():
            strRep = strRep+'\n'+'\t'*depth+" "+desc.__str__()
        strRep = strRep+"\n"+"\t"*depth+"Children: " + \
                                        str(len(self.get_children()))
        for child in self.get_children():
            strRep = strRep+'\n'+"\t"*(depth+1)+child.__str__(depth=depth+1)
        if len(self.get_children()) == 0:
            strRep += '\n'
        return strRep

    def __eq__(self, other):
        eq = isinstance(other, Family)
        eq = eq and self.get_children() == other.get_children()
        eq = eq and self.get_descs() == other.get_descs()
        return eq

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

    def _key_conflict(self, new_key):
        for entry in self.descs:
            if entry.get_key() == new_key:
                return True
        return False

    def _uniq_child(self, new_child):
        if len(self.get_children() == 0):
            return True
        for child in self.children:
            if child == new_child:
                return False
            if isinstance(child, Family):
                return self._uniq_child(new_child)

    def _check_recursion(self, seen=[]):
        if self in seen:
            return False
        if isinstance(self, FilePointer):
            return
        if len(self.children) == 0:
            return
        seen.append(self)
        for child in self.children:
            child._check_recursion(seen=seen)
        return True

    def set_children(self, new_children):
        assert(isinstance(new_children, list))
        for entry in new_children:
            assert(
                isinstance(entry, Family) or
                isinstance(entry, FilePointer)
            )
        self.children = new_children
        assert(self._check_recursion())

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
        assert(not self._key_conflict(keyValuePair.get_key()))
        if index is None:
            self.descs.append(keyValuePair)
        else:
            assert(isinstance(index, int))
            assert(index > -1 and index < len(self.descs))
            self.descs.insert(index, keyValuePair)

    def remove_desc(self, key_to_del=None, value_to_del=None, index=None):
        assert(bool(key_to_del) + bool(value_to_del) + bool(index) == 1)  # xor
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
        assert(isinstance(new_descs, KeyValuePairList))
        for entry in new_descs:
            assert(isinstance(entry, KeyValuePair))
        self.descs = new_descs

    def get_descs(self):
        return self.descs

    def get_desc(self, key=None, value=None, index=None):
        returns = self.get_desc_or(key=key, value=value, index=index)
        return returns

    def get_desc_or(self, key=None, value=None, index=None):
        returns = []
        cur_index = -1
        for desc in self.descs:
            cur_index += 1
            if desc.get_key() == key or \
                    desc.get_value() == value or \
                    cur_index == index:
                returns.append(desc)
        return returns

    def get_desc_and(self, key=None, value=None, index=None):
        returns = []
        cur_index = -1
        for desc in self.descs:
            cur_index += 1
            match = 0
            if key is not None and key == desc.get_key():
                match += 1
            if value is not None and value == desc.get_value():
                match += 1
            if index is not None and cur_index == index:
                match += 1
            if match == 3:
                returns.append(desc)
        return returns

    def write(self, path=getcwd(), file_name=None, clobber=False):
        if file_name is None:
            file_name = str(hash(self))+'.family'
        assert(isinstance(path, str))
        assert(isinstance(file_name, str))
        assert(isinstance(clobber, bool))
        assert(isdir(path))
        if clobber is False:
            assert(not exists(join(path, file_name)))
        dump(self, open(join(path, file_name), 'wb'))
