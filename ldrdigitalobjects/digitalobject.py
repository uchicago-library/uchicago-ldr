
from collections import namedtuple
from files import File
from re import compile as re_compile

class ControlTemplate(object):
    pattern = re_compile("(.*)")
    patternLabels = [namedtuple("identifierPart","label placement")]

    def __init__(self, objectPattern, patternLabels):
        self.pattern = re_compile(pattern)
        self.patternLabels = patternLabels

    def validateFilePath(self, filePath):
        assert exists(filePath)
        if self.pattern:
            pass

class DigitalObject(object):
    controlled = False
    controlTemplate = None
    identifier = None
    files = set([])

    def __iter__(self):
        for i in self.files:
            yield i
        
    def __init__(self, idValue):
        self.identifier = idValue

    def addFile(self,fObject):
        assert isinstance(fObject, File)
        if self.controlled:
            self.controlTemplate.validateFilepath(self.fObject.canonicalPath)
        else:
            self.files.add(fObject)

    def removeFile(self, fObject):
        assert isinstance(fObject, File)
        try:
            self.files.remove(fObject)
        except KeyError:
            return False
        return True

    def setAsControlled(self, template):
        assert isinstance(template, ControlTemplate)
        self.controlled = True
        self.controlTemplate = template
        
    def __repr__(self):
        prefix = "controlled object " if self.controlled \
                 else "uncontrolled object "
        return "<" + prefix + DigitalObject + self.identifier + " has " + \
            str(len(self.files)) + " files>"

    def __str__(self):
        prefix = "controlled object " if self.controlled else "uncontrolled "
        suffix = " file" if len(self.files) == 1 else " files"
        return prefix + self.identifier + " has " + str(len(self.files)) + \
            suffix

