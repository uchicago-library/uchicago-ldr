
from files import XML, Binary, Textual, File
from digitalobject import DigitalObject

# class DigitalObject(object):
#     controlled = False
#     controlTemplate = None
#     identifier = None
#     files = set([])

#     def __iter__(self):
#         for i in self.files:
#             yield i
        
#     def __init__(self, idValue):
#         self.identifier = idValue

#     def addFile(self,fObject):
#         assert isinstance(fObject, File)
#         self.files.add(fObject)

#     def removeFile(self, fObject):
#         assert isinstance(fObject, File)
#         try:
#             self.files.remove(fObject)
#         except KeyError:
#             return False
#         return True

#     def __repr__(self):
#         prefix = "controlled object " if self.controlled \
#                  else "uncontrolled object "
#         return "<" + prefix + DigitalObject + self.identifier + " has " + \
#             str(len(self.files)) + " files>"

#     def __str__(self):
#         prefix = "controlled object " if self.controlled else "uncontrolled "
#         suffix = " file" if len(self.files) == 1 else " files"
#         return prefix + self.identifier + " has " + str(len(self.files)) + \
#             suffix
    
if __name__ == "__main__":
    d = DigitalObject("foo")
    
    x = XML("./test.xml", '/home/tdanstrom/src/apps/')
    b = Binary("./foo.jpg", '/home/tdanstrom/src/apps/')
    t = Textual("./biz.txt", '/home/tdanstrom/src/apps/')
    e = Textual("./bob.txt", '/home/tdanstrom/src/apps/')
    f = Binary("./foo.gif", '/home/tdanstrom/src/apps/')
    g = Binary("./boo.tif", '/home/tdanstrom/src/apps/')

    d.addFile(x)
    d.addFile(b)
    d.addFile(t)
    d.addFile(f)
    d.addFile(e)
    d.addFile(g)
    print(d.controlled)
    for n in d:
        print(n.filepath)
        print(n.calculateCanonicalPath('/home/tdanstrom/src/apps'))
        print(n.canonicalPath)

        print(n.checksum.digestValue)
    print(d)

    d.removeFile(f)

    print(d)
