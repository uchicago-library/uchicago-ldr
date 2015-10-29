from re import escape,split
from collections import Counter

from uchicagoldr.item import Item

class TextItem(Item):

    raw_string=None
    term_index=None
    term_pruning_function=None

    def __init__(self,path,root):
        Item.__init__(self,path,root)

    def find_raw_string(self):
        with open(self.filepath,'r',errors='replace') as f:
            raw_string=f.read()
        return raw_string.lower()

    def get_raw_string(self):
        return self.raw_string

    def set_raw_string(self,newString):
        self.raw_string=newString

    def set_term_pruning_function(self,newFunction):
        self.term_pruning_function=newFunction

    def get_term_pruning_function(self):
        return self.term_pruning_function

    def find_index(self,purge_raw=False,term_map=None):
        assert(self.get_raw_string() != None)
        fileString=self.get_raw_string()
        regexPattern = '|'.join(map(escape, [" ","\n",".",",",";","'","-","\t","?","!",'(',')','[',']''\\',":","\"","\'",'“','—',"‘","’","”","#","…","/","|","*"]))
        termList=split(regexPattern,fileString)
        if purge_raw:
            self.set_raw_string(None)
        if self.term_pruning_function is not None:
            self.term_pruning_function(termList)
        if term_map != None:
            i=0
            for term in termList:
                if term in term_map:
                    termList[i]=term_map[term]
                else:
                    term_map[term]=len(term_map)+1
                i+=1
        index=Counter()
        for term in termList:
            index[term]+=1
        return index

    def get_index(self):
        return self.index

    def set_index(self,newIndex):
        assert(isinstance(newIndex,Counter))
        self.index=newIndex
