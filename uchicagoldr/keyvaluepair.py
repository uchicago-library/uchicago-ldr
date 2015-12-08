class KeyValuePair(object):

    key = None
    value = None
    nested = False
    objHash = None

    def __init__(self, key, value=""):
        assert(isinstance(key, str))
        assert(isinstance(value, str) or
               isinstance(value, int) or
               isinstance(value, float) or
               isinstance(value, complex) or
               isinstance(value, KeyValuePair)
               )
        if isinstance(value, KeyValuePair):
            self.nested = True
        self.key = key
        self.value = value
        self.objHash = (hash(key) << 1) ^ hash(value)

    def __eq__(self, other):
        return isinstance(other, KeyValuePair) and hash(other) == hash(self)

    def __hash__(self):
        return self.objHash

    def __repr__(self):
        return "[ {} : {} ]".format(self.key, self.value)

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def is_nested(self):
        return self.nested
