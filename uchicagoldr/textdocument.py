from uchicagoldr.item import Item
from re import escape, split


class TextDocument(Item):
    """
    A sublass of the item class, meant to potentially aid with text analysis
    """
    unique_terms = []
    terms = []
    term_counts = []

    def __init__(self, path, root):
        Item.__init__(self, path, root)

    def find_terms(self):
        with open(self.filepath, 'r', errors='replace') as f:
            fileString = f.read()
        fileString = fileString.lower()
        regexPattern = '|'.join(map(escape, [" ", "\n", ".", ",", ";", "'",
                                             "-", "\t", "?", "!", '(', ')',
                                             '[', ']', '\\']))
        splitString = split(regexPattern, fileString)
        return splitString

    def set_terms(self, newTerms):
        self.terms = newTerms

    def get_terms(self):
        return self.terms

    def find_unique_terms(self):
        assert(self.terms)
        uniqueTerms = set(self.terms)
        return uniqueTerms

    def set_unique_terms(self, newUnique):
        self.unique_terms = newUnique

    def get_unique_terms(self):
        return self.unique_terms

    def find_term_counts(self):
        assert(self.terms)
        counts = []
        uniques = self.find_unique_terms()
        for term in uniques:
            counts.append((term, self.terms.count(term)))
        return counts

    def set_term_counts(self, newCounts):
        self.term_counts = newCounts

    def get_term_counts(self):
        return self.term_counts

    def find_term_idfs(self):
        assert(isinstance(self.get_batch(),TextBatch))
        assert(len(self.get_terms())>0)
        assert(len(self.get_batch().get_idfs())>0)
        idfsubset={}
        for term in self.get_terms():
            if term in self.get_batch().get_terms():
                idfsubset[term]=batch.get_idfs()[term]
        return idfsubset

    def set_term_idfs(self,newidfs):
        self.term_idfs=newidfs

    def get_term_idfs(self):
        return self.term_idfs()

    def find_tf_idfs(self):
        return self.get_batch().get_item_tf_idfs()[self.get_file_path()]

    def get_tf_idfs(self):
        return self.tfidfs

    def set_tf_idfs(self,newTFIDFS):
        self.tfidfs=newTFIDFS

    def find_vector_space_model(self):
        normalizedVectorLengths={}
        edgeLength=0
        for term in self.get_tf_idfs():
            edgeLength+=self.get_tf_idfs()[term]**2
        vectorLength=edgeLength**.5
        for term in self.get_tf_idfs():
            normalizedVectorLengths[term]=self.get_tf_idfs()[term]/vectorLength
        return normalizedVectorLengths

    def get_vector_space_model(self):
        return self.vsm

    def set_vector_space_model(self,new_vsm):
        self.vsm=new_vsm
