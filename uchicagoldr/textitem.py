from re import escape,split
from collections import Counter

from uchicagoldr.item import Item
from uchicagoldr.textprocessingfunctions import *

class TextItem(Item):

    raw_string=None
    term_index=None

    def __init__(self,path,root):
        Item.__init__(self,path,root)

    def find_raw_string(self):
        with open(self.filepath,'r',errors='replace') as f:
            raw_string=f.read()
        return raw_string

    def get_raw_string(self):
        return self.raw_string

    def set_raw_string(self,newString):
        self.raw_string=newString

    def find_index(self,purge_raw=False,term_map=None,scrub_text=False,stem=False,only_mapped=False):
        assert(self.get_raw_string() != None)
        fileString=self.get_raw_string()
        regexPattern = '|'.join(map(escape, [" ","\n",".",",",";","'","-","\t","?","!",'(',')','[',']''\\',":","\"","\'",'“','—',"‘","’","”","#","…","/","|","*"]))
        termList=split(regexPattern,fileString)
        if stem == True:
            termList=stemTerms(termList)
        if scrub_text:
            termList=minOccurence(stopTerms(percChar(maxLength(minLength(noDigits(lowerCase(termList)))))))
        if purge_raw:
            self.set_raw_string(None)
        if term_map != None:
            i=0
            for term in termList:
                if term in term_map:
                    termList[i]=term_map[term]
                else:
                    if only_mapped:
                        del termList[i]
                    else:
                        termList[i]=len(term_map)
                        term_map[term]=len(term_map)
                i+=1
        index=Counter()
        for term in termList:
            index[term]+=1
        return index,term_map

    def get_index(self):
        return self.index

    def set_index(self,newIndex):
        assert(isinstance(newIndex,Counter))
        self.index=newIndex
