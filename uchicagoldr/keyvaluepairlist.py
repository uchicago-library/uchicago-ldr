from collections.abc import MutableSequence

from uchicagoldr.keyvaluepair import KeyValuePair


class KeyValuePairList(MutableSequence):
    def __init__(self):
        self.innerList = []

    def __getitem__(self, index):
        try:
            return self.innerList[index]
        except Exception as e:
            raise e

    def __setitem__(self, index, value):
        if not isinstance(value, KeyValuePair):
            raise ValueError

        try:
            self.innerList.insert(index, value)
        except Exception as e:
            raise e

    def __delitem__(self, index):
        try:
            del self.innerList[index]
        except Exception as e:
            raise e

    def __len__(self):
        return len(self.innerList)

    def __repr__(self):
        return self.innerList.__repr__()

    def __str__(self):
        return str(self.innerList)

    def insert(self, index, value):
        if not isinstance(value, KeyValuePair):
            raise ValueError
        try:
            self.innerList.insert(index, value)
        except Exception as e:
            raise e

    def append(self, value):
        if not isinstance(value, KeyValuePair):
            raise ValueError
        try:
            self.innerList.append(value)
        except Exception as e:
            raise e

    def extend(self, values):
        for v in values:
            if not isinstance(v, KeyValuePair):
                raise ValueError
            self.innerList.append(v)

    def keys(self):
        keyList = []
        for kvp in self.innerList:
            keyList.append(kvp.get_key())
        return keyList

    def values(self):
        valueList = []
        for kvp in self.innerList:
            valueList.append(kvp.get_value())
        return valueList
