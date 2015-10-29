from collections import deque, namedtuple
from hashlib import md5, sha256
from magic import from_file
from os.path import abspath, exists, relpath
from re import compile as re_compile

class Checksum(object):
    checksum = None
    value = None

    def __init__(self):
        self.digestType = None
        self.digestValue = None

    def calculateSha256Digest(self, filepath):
        blocksize = 650236
        hash = sha256()
        afile = open(filepath,'rb')
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hash.update(buf)
            buf = afile.read(blocksize)
        self.digestType = 'sha256'
        self.digestValue = hash.hexdigest()     

    def calculateMd5Digest(self, filepath):
        blocksize = 650236
        hash = md5()
        afile = open(filepath,'rb')
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hash.update(buf)
            buf = afile.read(blocksize)
        self.digestType = 'md5'
        self.digestValue = hash.hexdigest()             
        return True

class File(object):
    mimeType = None
    filePath = namedtuple("fixityDigest","digestType digestValue")
    canonicalPath = None
    fileSize = None
    riskLevel = None

    def __init__(self, filepath, root):
        assert exists(filepath)
        self.filepath = filepath
        self.calculateCanonicalPath(root)
        self.calculateChecksum('sha256')
        self.fileSize = None
        self.riskLevel = None
        self.mimeType = None
        
    def calculateChecksum(self, fixityType):
        assert fixityType in ['sha256','md5']
        c = Checksum()
        if fixityType == 'sha256':
            c.calculateSha256Digest(self.filepath)
        else:
            c.calculateMd5Digest(self.filepath)
        if c:
            self.checksum = c
            return True
        return None
    
    def calculateFileSize(self):
        self.fileSize = stat(self.filpath).st_size
        return True
    
    def calculateMimeType(self):
        self.mimeType = from_file(self.filpath, mimetype=True)

    def calculateCanonicalPath(self, extraneousPathPart):
        path = abspath(self.filepath)
        path = relpath(self.filepath, extraneousPathPart)
        
        header_pattern = '^\d{4}-\d{3}'
        if re_compile(header_pattern).search(path):
            self.canonicalPath = re_split(path, header_pattern)[1]
            return True
        else:
            self.canonicalPath = path
            return True
        return None
    
    def getFileSize(self):
        return self.fileSize

    def getFilePath(self):
        return self.filePath

    def getRiskLevel(self):
        return self.riskLevel

    def getMimeType(self):
        return self.mimeType

class XML(File):
    schema = None
    namespace = None
    keyElements = set([])


class Textual(File):
    keyWords = None


class Binary(File):
    requirement = None
