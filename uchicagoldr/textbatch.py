from collections import Counter

from uchicagoldr.batch import Batch
from uchicagoldr.textdocument import TextDocument

class TextBatch(Batch):
    """
    A subclass of the batch class, meant to potentially aid with text analysis
    """
    terms=[]
    unique_terms=[]
    term_counts=[]
    doc_counts=[]
    tf_idfs=[]

    def __init__(self,path,root):
        Batch.__init__(self,root,path)

    def validate_items(self):
        for item in self.get_items():
            try:
                assert isinstance(item,TextDocument)
            except AssertionError:
                return False
        return True

    def find_terms(self):
        itemTerms=[]
        for item in self.get_items():
            assert isinstance(item,TextDocument)
            item.set_terms(item.find_terms())
            itemTerms+=item.get_terms()
        return itemTerms

    def set_terms(self,newTerms):
        self.terms=newTerms

    def get_terms(self):
        return self.terms

    def find_doc_counts(self):
        assert(self.unique_terms is not [])
        counts=Counter()
        for term in self.unique_terms:
            for item in self.get_items():
                if term in item.get_terms():
                    counts[term]+=1
        return counts

    def set_doc_counts(self,newCounts):
        self.doc_counts=newCounts

    def get_doc_counts(self):
        return self.doc_counts

    def find_unique_terms(self):
        assert(self.terms is not [])
        uniqueTerms=set(self.terms)
        return uniqueTerms

    def set_unique_terms(self,newUnique):
        self.unique_terms=newUnique

    def get_unique_terms(self):
        return self.unique_terms

    def find_term_counts(self):
        assert(self.terms is not [])
        counts=[]
        uniques=self.find_unique_terms()
        for term in uniques:
            counts.append((term,self.terms.count(term)))
        return counts

    def set_term_counts(self,newCounts):
        self.term_counts=newCounts

    def get_term_counts(self):
        return self.term_counts
