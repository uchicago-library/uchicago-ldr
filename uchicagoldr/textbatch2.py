from collections import Counter
from math import log

from uchicagoldr.batch import Batch
from uchicagoldr.textitem import TextItem

class TextBatch(Batch):

    term_index=None
    doc_counts=None
    idfs=None
    iIdfs=None
    tf_idfs=None
    language_model=None
    vsm=None
    doc_vsms=None
    term_map={}

    def __init__(self,path,root):
        Batch.__init__(self,root,path)

    def validate_items(self):
        for item in self.get_items():
            try:
                assert(isinstance(item,TextItem))
            except AssertionError:
                return False
        return True

    def find_term_index(self):
        index=Counter()
        for item in self.get_items():
            index+=item.get_index()
        return index

    def get_term_index(self):
        return self.term_index

    def set_term_index(self,newIndex):
        assert(isinstance(newIndex,Counter))
        self.term_index=newIndex

    def find_doc_counts(self):
        counts=Counter()
        for item in self.get_items():
            for term in item.get_index():
                counts[term]+=1
        return counts

    def get_doc_counts(self):
        return self.doc_counts

    def set_doc_counts(self,newCounts):
        assert(isinstance(newCounts,Counter))
        self.doc_counts=newCounts

    def find_idfs(self):
        termIDFs={}
        for term in self.find_doc_counts():
            IDF=log(1+(len(self.get_items())/self.get_doc_counts()[term]))
            termIDFs[term]=IDF
        return termIDFs

    def get_idfs(self):
        return self.idfs

    def set_idfs(self,newIDFs):
        assert(isinstance(newIDFs,dict))
        self.idfs=newIDFs

    def find_iIdfs(self):
        termIIDFs={}
        for term in self.find_doc_counts():
            IIDF=1+(self.get_doc_counts()[term]/len(self.get_items()))
            termIIDFs[term]=IIDF
        return termIIDFs

    def get_iIdfs(self):
        return self.iIdfs

    def set_iIdfs(self,newIIDFS):
        assert(isinstance(newIIDFS,dict))
        self.iIdfs=newIIDFS

    def find_tf_idfs(self):
        k=.5
        itemTFIDFs={}
        termIDFs=self.get_idfs()
        for item in self.get_items():
            termTFIDFs={}
            if len(item.get_index())==0:
               itemTFIDFs[item.get_file_path()]=termTFIDFs 
            else:
                maxTerm=item.get_index().most_common()[0][1]
                for term in item.get_index():
                    tf=k+(1-k)*(item.get_index()[term]/maxTerm)
                    idf=self.idfs[term]
                    termTFIDFs[term]=tf*idf
                itemTFIDFs[item.get_file_path()]=termTFIDFs
        return itemTFIDFs

    def get_tf_idfs(self):
        return self.tf_idfs

    def set_tf_idfs(self,newTFIDFs):
        assert(isinstance(newTFIDFs,dict))
        self.tf_idfs=newTFIDFs

    def find_language_model(self):
        k=.5
        language_model={}
        maxTerm=self.get_term_index().most_common()[0][1]
        for term in self.get_term_index():
            tf=k+(1-k)*(self.get_term_index()[term]/maxTerm)
            iIdf=self.iIdfs[term]
            language_model[term]=tf*iIdf
        return language_model

    def get_language_model(self):
        return self.language_model

    def set_language_model(self,newlm):
        assert(isinstance(newlm,dict))
        self.language_model=newlm

    def find_document_vector_space_models(self):
        docVSMs={}
        for item in self.get_items():
            normalizedVectorLengths={}
            squaredSum=0
            for term in item.get_index():
               squaredSum+=self.get_tf_idfs()[item.get_file_path()][term]**2
            hypot=squaredSum**.5
            for term in item.get_index():
                normalizedVectorLengths[term]=self.get_tf_idfs()[item.get_file_path()][term]/hypot
            docVSMs[item.get_file_path()]=normalizedVectorLengths
        return docVSMs

    def get_document_vector_space_models(self):
        return self.doc_vsms

    def set_document_vector_space_models(self,newDocVSMs):
        assert(isinstance(newDocVSMs,dict))
        self.doc_vsms=newDocVSMs

    def find_vector_space_model(self):
        normalizedVectorLengths={}
        squaredSum=0
        for term in self.get_term_index():
            squaredSum+=self.get_language_model()[term]**2
        hypot=squaredSum**.5
        for term in self.get_term_index():
            normalizedVectorLengths[term]=self.get_language_model()[term]/hypot
        return normalizedVectorLengths

    def get_vector_space_model(self):
        return self.vsm

    def set_vector_space_model(self,newVSM):
        assert(isinstance(newVSM,dict))
        self.vsm=newVSM

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
