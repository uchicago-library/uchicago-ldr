
from collections import namedtuple
from files import File
from re import compile as re_compile

class ControlTemplate(object):
    pattern = re_compile("(.*)")
    patternLabels = [namedtuple("identifierPart","label placement")]

    def __init__(self, pattern, patternLabels):
        self.pattern = re_compile(pattern)
        self.patternLabels = []

    def addLabel(self, labelName, labelPosition):
        assert isinstance(labelName, str)
        assert isinstance(labelPosition, str)
        o = namedtuple("identifierPart","label placement") \
            (labelName,labelPosition)
        return o

    def validateFilePath(self, filePath):
        if self.pattern:
            pass

class DigitalObject(Batch):
    controlled = True
    controlTemplate = None
    identifier = None

    def __init__(self, identifier, template):
        assert isinstance(template, ControlTemplate)
        self.identifier = identifier
        self.controlTemplate = controlTemplate

    def addFile(self,fObject):
        assert isinstance(fObject, File)
        if self.controlTemplate.validateFilepath(self.fObject.canonicalPath):
            self.files.add(fObject)
            return True
        return False

