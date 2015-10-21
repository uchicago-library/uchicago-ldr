from re import escape,split
from collections import Counter

from uchicagoldr.item import Item

class TextDocument(Item):
    """
    A sublass of the item class, meant to potentially aid with text analysis
    """
    raw_string=""
    unique_terms=[]
    terms=[]
    term_counts=Counter()
    term_idfs={}
    
    def __init__(self,path,root):
        Item.__init__(self,path,root)

    def find_raw_string(self):
        assert(len(self.get_file_path())>0)
        with open(self.filepath,'r',errors='replace') as f:
            raw_string=f.read()
        return raw_string

    def get_raw_string(self):
        return self.raw_string

    def set_raw_string(self,new_raw_string):
        self.raw_string=new_raw_string

    def find_terms(self):
        assert(len(self.get_raw_string())>0)
        fileString=self.get_raw_string().lower()
        regexPattern = '|'.join(map(escape, [" ","\n",".",",",";","'","-","\t","?","!",'(',')','[',']''\\',":","\"","\'",'“','—',"‘","’","”","#","…","/","|","*"]))
        splitString=split(regexPattern,fileString)
        return splitString

    def set_terms(self,newTerms):
        self.terms=newTerms

    def get_terms(self):
        return self.terms

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
        return counts

    def set_term_counts(self,newCounts):
        self.term_counts=newCounts

    def get_term_counts(self):
        return self.term_counts

    def find_term_idfs(self,batch):
        assert(isinstance(batch,TextBatch))
        assert(len(self.get_terms())>0)
        assert(len(batch.get_idfs())>0)
        idfsubset={}
        for term in self.get_terms():
            if term in batch.get_terms():
                idfsubset[term]=batch.get_idfs()[term]
        return idfsubset
        
    def set_term_idfs(self,newidfs):
        self.term_idfs=newidfs

    def get_term_idfs(self):
        return self.term_idfs()
