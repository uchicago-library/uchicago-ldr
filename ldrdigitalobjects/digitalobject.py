
from collections import namedtuple
from files import File
from re import compile as re_compile

class ControlTemplate(object):
    pattern = re_compile("(.*)")
    patternLabels = [namedtuple("identifierPart","label placement")]

    def __init__(self, pattern, patternLabels):
        self.pattern = re_compile(pattern)
        self.patternLabels = []

    def addLabel(self, labelName, labelPosition, labelPattern):
        assert isinstance(labelName, str)
        assert isinstance(labelPosition, str)
        o = namedtuple("identifierPart","label placement pattern") \
            (labelName, labelPosition, labelPattern)
        return o

    def validateFilePath(self, filePath):
        for patternData in self.patternLabels:
            if re_compile(patternData.pattern).match(filePath):
                return patternData.labelName
        return False

class DigitalObject(Batch):
    controlled = True
    controlTemplate = None
    identifier = None

    def __init__(self, identifier, template):
        assert isinstance(template, ControlTemplate)
        self.identifier = identifier
        self.controlTemplate = controlTemplate

    def addFile(self, fObject):
        assert isinstance(fObject, File)
        definedPart = self.controlTemplate.validateFilepath \
                      (self.fObject.canonicalPath):
        if definedPart:
            dopart = namedtuple("digitalObjectPart","partLabel partFile") \
                     (definedPart, fObject)
            self.files.add(dopart)
            return True
        return False

    def removeFile(self, fObject):
        return False
