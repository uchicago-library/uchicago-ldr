from uchicagoldr.file import File


class FilePointer(object):

    identifier = None

    def __init__(self, identifier):
        assert(isinstance(identifier, str))
        self.identifier = identifier

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return (isinstance(other, FilePointer) and
                hash(self) == hash(other))

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, newIdentifier):
        assert(isinstance(newIdentifier, str))
        self.identifier = newIdentifier

    def look_up_file(self):
        # Return a reference to the File object
        pass
