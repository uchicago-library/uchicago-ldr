from collections import Counter
from math import log

from uchicagoldr.batch import Batch
from uchicagoldr.textdocument import TextDocument

class TextBatch(Batch):
    """
    A subclass of the batch class, meant to potentially aid with text analysis
    """
    terms=[]
    unique_terms=[]
    term_counts=[]
    doc_counts=Counter()
    idfs={}
    tf_idfs={}
    batch_tf_idfs={}
    vsm={}

    def __init__(self,path,root):
        Batch.__init__(self,root,path)

    def validate_items(self):
        assert(len(self.get_items())>0)
        for item in self.get_items():
            try:
                assert isinstance(item,TextDocument)
            except AssertionError:
                return False
        return True

    def find_terms(self):
        assert(len(self.get_items())>0)
        itemTerms=[]
        for item in self.get_items():
            assert isinstance(item,TextDocument)
            item.set_raw_string(item.find_raw_string())
            item.set_terms(item.find_terms())
            itemTerms+=item.get_terms()
        return itemTerms

    def set_terms(self,newTerms):
        self.terms=newTerms

    def get_terms(self):
        return self.terms

    def find_doc_counts(self):
        assert(len(self.unique_terms)>0)
        assert(len(self.get_items())>0)
        counts=Counter()
        for item in self.get_items():
            item.set_terms(item.find_terms())
            item.set_unique_terms(item.find_unique_terms())
            for term in item.get_unique_terms():
                counts[term]+=1
        return counts

    def set_doc_counts(self,newCounts):
        self.doc_counts=newCounts

    def get_doc_counts(self):
        return self.doc_counts

    def find_unique_terms(self):
        assert(len(self.get_terms())>0)
        uniqueTerms=set(self.terms)
        return uniqueTerms

    def set_unique_terms(self,newUnique):
        self.unique_terms=newUnique

    def get_unique_terms(self):
        return self.unique_terms

    def find_term_counts(self):
        assert(len(self.get_terms())>0)
        assert(len(self.get_unique_terms())>0)
        counts=Counter(self.get_terms())
#        uniques=self.get_unique_terms()
#        for term in uniques:
#            counts[term]=self.terms.count(term)
        return counts

    def set_term_counts(self,newCounts):
        self.term_counts=newCounts

    def get_term_counts(self):
        return self.term_counts

    def find_idfs(self):
        termIDFS={}
        for term in self.get_unique_terms():
            IDF=log(1+(len(self.get_items())/self.get_doc_counts()[term]))
            termIDFS[term]=IDF
        return termIDFS

    def get_idfs(self):
        return self.idfs

    def set_idfs(self,newIDFS):
        self.idfs=newIDFS

    def find_item_tf_idfs(self):
        assert(len(self.get_items())>0)
        assert(len(self.get_unique_terms())>0)
        assert(len(self.get_idfs())>0)
        k=.5
        itemTFIDFS={}
        termIDFS=self.get_idfs()
        for item in self.get_items():
            item.set_raw_string(item.find_raw_string())
            item.set_terms(item.find_terms())
            item.set_unique_terms(item.find_unique_terms())
            item.set_term_counts(item.find_term_counts())
            maxTerm=item.get_term_counts().most_common()[0][1]
            tfidfs={}
            for term in item.get_unique_terms():
                if term in self.get_unique_terms():
                    tf =k+(1-k)*(item.get_term_counts()[term]/maxTerm)
                    idf=termIDFS[term]
                    tfidfs[term]=tf*idf
            itemTFIDFS[item.get_file_path()]=tfidfs
        return itemTFIDFS

    def get_item_tf_idfs(self):
        return self.tf_idfs

    def set_item_tf_idfs(self,newTFIDFs):
        assert isinstance(newTFIDFs,dict)
        self.tf_idfs=newTFIDFs

    def find_batch_tf_idfs(self):
        assert(len(self.get_term_counts())>0)
        assert(len(self.get_unique_terms())>0)
        assert(len(self.get_items())>0)
        assert(len(self.get_term_counts())>0)
        k=.5
        maxTerm=self.get_term_counts().most_common()[0][1]
        batchTFIDFs=self.get_idfs()
        for term in self.get_unique_terms():
            IDF=batchTFIDFs[term]
            tf=k+(1-k)*(self.get_term_counts()[term]/maxTerm)
            tfidf=tf*IDF
            batchTFIDFs[term]=tfidf
        return batchTFIDFs

    def get_batch_tf_idfs(self):
        return self.batch_tf_idfs

    def set_batch_tf_idfs(self,new_batch_tf_idfs):
        assert(isinstance(new_batch_tf_idfs,dict))
        self.batch_tf_idfs=new_batch_tf_idfs

    def find_vector_space_model(self):
        assert(len(self.get_batch_tf_idfs())>0)
        normalizedVectorLengths={}
        edgeLength=0
        for term in self.get_batch_tf_idfs():
            edgeLength+=self.get_batch_tf_idfs()[term]**2
        vectorLength=edgeLength**.5
        for term in self.get_batch_tf_idfs():
            normalizedVectorLengths[term]=self.get_batch_tf_idfs()[term]/vectorLength
        return normalizedVectorLengths

    def get_vector_space_model(self):
        return self.vsm

    def set_vector_space_model(self,new_vsm):
        self.vsm=new_vsm

    def find_similarity(self,other_vsm):
        simVec={}
        simPerc=0
        if len(self.get_vector_space_model())>len(other_vsm):
            for term in other_vsm:
                if term in self.get_vector_space_model():
                    simVec[term]=self.get_vector_space_model()[term]*other_vsm[term]
        else:
            for term in self.get_vector_space_model():
                if term in other_vsm:
                    simVec[term]=self.get_vector_space_model()[term]*other_vsm[term]
        for term in simVec:
            simPerc+=simVec[term]
        return simPerc
