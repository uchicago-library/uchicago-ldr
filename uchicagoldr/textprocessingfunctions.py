from collections import Counter

from stemming.porter2 import stem

def pruneTerms(terms):
    newTerms=minOccurence(minLength(maxLength(percChar(stopTerms(noDigits(lowerCase(terms)))))))
    return newTerms

def stemTerms(terms):
    newTerms=[]
    for term in terms:
        newTerms.append(stem(term))
    return newTerms

def stopTerms(terms,stopList=None):
    if stopList is None:
        stopList=['','the','and','if','then','when','to','of','in','a','i','that','received','was','as','is','you','with','this','were','not','has','"','it','at','he','contents','earthlink','received','*','she','id','we','yahoo','http://www','my','for','am','her','from','have','on','received','be','content-type:','would','they','edu','are','by','been','had','our','an','will','com','or','who','me','who','about','your','his','but','university','chicago','re:','do','mr','could','uchicago','midway','(8','received:','esmtp','so','can','bsd','subject:','(cst)','there','which','no','yes','smtp','date:','them','said','smtp','from:','to:','net','very','also','org','no','all','there','&nbsp''(cdt)','their','ms','mrs','ll','how','org','one','what','us','those','into','what','more','those','into','because','pp','out','than','many','any','only','some','such','its','these',"new","must",'way','up','ve','again','too','fwd']
    stopList=set(stopList)
    newTerms=[]
    for term in terms:
        if term in stopList:
            continue
        newTerms.append(term)
    return newTerms

def lowerCase(terms):
    newTerms=[]
    for term in terms:
        newTerms.append(term.lower())
    return newTerms

def percChar(terms,percent=51):
    newTerms=[]
    for term in terms:
        if len(term)>0:
            percChar=sum(c.isalpha() for c in term)/float(len(term))
            if percChar < (percent/100):
                continue
            newTerms.append(term)
    return newTerms

def noDigits(terms):
    newTerms=[]
    for term in terms:
        if term.isdigit():
            continue
        newTerms.append(term)
    return newTerms

def maxLength(terms,maxLength=20):
    newTerms=[]
    for term in terms:
        if len(term) > maxLength:
            continue
        newTerms.append(term)
    return newTerms

def minLength(terms,minLength=2):
    newTerms=[]
    for term in terms:
        if len(term) < minLength:
            continue
        newTerms.append(term)
    return newTerms

def minOccurence(terms,minOccurences=2):
    newTerms=[]
    termsSeen=Counter(terms)
    for term in terms:
        if termsSeen[term] < minOccurences:
            continue
        newTerms.append(term)
    return newTerms

def maxOccurence(terms,maxOccurences=9001):
    newTerms=[]
    termsSeen=Counter(terms)
    for terms in termsSeen:
        if termsSeen[term] > maxOccurences:
            continue
        newTerms.append(term)
    return newTerms
