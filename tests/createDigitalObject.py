
from ldrdigitalobjects.files import XML, Binary, Textual, File
from ldrdigitalobjects.digitalobject import ControlTemplate, DigitalObject
from ldrdigitalobjects.batch import Batch

if __name__ == "__main__":
    b = Batch("bar")
    t = ControlTemplate("limb-campub")

    d = DigitalObject("first_object",t)
    
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

    for n in d:
        print(n.filepath)
        print(n.calculateCanonicalPath('/home/tdanstrom/src/apps'))
        print(n.canonicalPath)

        print(n.checksum.digestValue)
    print(d)

    d.removeFile(f)

    print(d)
