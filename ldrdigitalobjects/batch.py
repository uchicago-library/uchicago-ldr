
from files import File

class Batch(object):
    identifier = None
    files = set([])

    def __init__(self, idValue):
        self.identifier = idValue
        self.files = set([])

    def __iter__(self):
        for n in self.files:
            yield n

    def addFile(self, fObject):
        assert isinstance(fObject, File)
        self.files.add(fObject)

    def removeFile(self,fObject):
        assert isinstance(fObject, File)
        self.files.remove(fObject)

    def findFile(self, filePath):
        for n in self.files:
            if n.filePath == filePath:
                return n
        return False

    def __str__(self):
        return self.identifier

    def __repr__(self):
        a_string = "{id} with {numfiles}".format(id = self.identifier,
                                                 numfiles = len(self.files))
        return a_string
