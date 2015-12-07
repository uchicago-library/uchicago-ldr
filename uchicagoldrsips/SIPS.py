
from collections import namedtuple
from os.path import basename, join, splitext
from re import compile as re_compile
from sys import stdout, stderr

class Namespace(object):
    def __init__(self, ns, u):
       self.nspace = ns
       self.url = SubjectURL(u)

    def __str__(self):
        return "@prefix {ns}: {url}.\n".format(ns=self.nspace, url=str(self.url))

class BaseNamespace(object):
    url = None
    def __init__(self, u):
        self.url = SubjectURL(u)

    def __str__(self):
        return "@base {url}.\n".format(url = str(self.url))

class URL(object):
    def __str__(self):
        return "<"+str(self.subject)+">"

class SubjectURL(URL):
    def __init__(self, u):
        self.subject = u

class LDRURL(URL):
    def __init__(self, u):
        url = "http://ldr.lib.uchicago.edu/"
        url = join(url, u)
        self.subject = url

class RightsURL(URL):
    def __init__(self):
        self.subject = "http://creativecommons.org/licenses/by-nc/4.0/"

class PIURL(URL):
    def __init__(self, collection_ref, object_identifier):
        url = "http://pi.lib.uchicago.edu/1001/"
        url = join(url, collection_ref, object_identifier)
        self.subject = url

class Value(object):
    string = ""
    def __init__(self,value):
        self.string = value

    def __str__(self):
        return str(self.string)

class IntegerValue():
    def __init__(self, value):
        assert isinstance(value, int)
        self.string = value

    def __str__(self):
        return str(self.string)

class DateValue(Value):
    def __str__(self):
        return "\"\"\"{value}\"\"\"^^xsd:dateTime". \
            format(value = self.string)

class TextValue(Value):
    def __str__(self):
        return "\"{value}\"".format(value = self.string)

class Statement(object):
    def __init__(self, element, value):
        self.element = element
        self.value = value

    def __str__(self):
        return "{element} {value}".format(element = self.element,
                                          value = str(self.value))

class Triple(object):

    def add_statement(self, verb, value):
        assert len(verb.split(":")) == 2
        s = Statement(verb, value)
        self.statements.append(s)    

    def __str__(self):
        return "\n{subject}\n{statements};\na {type}.\n". \
            format(subject = str(self.subject),
                   type = self.object_type,
                   statements = ';\n'.join([str(x) for x in self.statements]))


class ProvidedCHO(Triple):
    def __init__(self, id):
        self.subject = SubjectURL(join("/", id))
        self.statements = []
        self.object_type = "edm:ProvidedCHO"

class Aggregation(Triple):
    def __init__(self, id):
        self.subject = SubjectURL(join("/aggregation", id))
        self.statements = []
        self.object_type = "ore:Aggregation"

class ResourceMap(Triple):
    def __init__(self, id):
        self.subject = SubjectURL(join('/rem', id))
        self.statements = []
        self.object_type = "ore:ResourceMap"

class Proxy(Triple):
    def __init__(self, id):
        self.subject = SubjectURL(join("/", id))
        self.statements = []
        self.object_type = "ore:Proxy"

class WebResource(Triple):
    def __init__(self, id):
        self.subject = SubjectURL(join("/", id))
        self.statements = []
        self.object_type = "edm:WebResource"

class RDFSResource(Triple):
    def __init__(self, id):
        self.subject = SubjectURL(join("/", id))
        self.statements = []
        self.object_type = "rdfs:Resource"
