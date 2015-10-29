
from collections import namedtuple
from files import File
from batch import Batch
from re import compile as re_compile

class ControlTemplate(object):
    pattern = re_compile("(.*)")
    patternLabels = [namedtuple("identifierPart","label placement")]

    def __init__(self,idValue):
        self.identifier = idValue
        self.patternLabels = []

    def addPart(self, labelName, labelPosition, labelPattern):
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

class Item(object):
    item = None

    def __init__(self,item):
        assert (isinstance(item, DigitalObject) or isinstance(item, File))
        self.item = item

    def getType(self):
        return type(self.item).__name__

    def getCanonicalPath(self):
        if isinstance(self.item, File):
            return self.item.canonicalPath
        return None

    def get

class DigitalObject(object):
    controlTemplate = None
    identifier = None
    description = ""
    items = []

    def __init__(self, identifier, template):
        assert isinstance(template, ControlTemplate)
        assert isinstance(identifier, str)
        self.identifier = identifier
        self.controlTemplate = template

    def describe(self, text):
        assert isinstance(text, str)
        self.describe = text

    def addItem(self, item):
        definedPart = self.controlTemplate.validateFilepath \
                      (self.fObject.canonicalPath)
        if definedPart:
            dopart = namedtuple("digitalObjectPart","partLabel partFile") \
                     (definedPart, fObject)
            self.files.add(dopart)
            return True
        return False

    def removeItem(self, fObject):
        return False

    def removeControlTemplate(self):
        self.controlTemplate = None

    def findFileByPath(self, path):
        for f in self.files:
            if f.partFile.canonicalPath ==  path:
                return f
        return False

    def findFileByPartName(self, partName):
        for f in self.files:
            if f.partLabel == partName:
                return f
        return False

