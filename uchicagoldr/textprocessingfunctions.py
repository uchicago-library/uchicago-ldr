def pruneTerms(terms):
    newTerms=[]
    stopList=['','the','and','if','then','when','to','of','in','a','i','that','received','was','as','is','you','with','this','were','not','has','"','it','at','he','contents','earthlink','received','*','she','id','we','yahoo','http://www','my','for','am','her','from','have','on','received','be','content-type:','would','they','edu','are','by','been','had','our','an','will','com','or','who','me','who','about','your','his','but','university','chicago','re:','do','mr','could','uchicago','midway','(8','received:','esmtp','so','can','bsd','subject:','(cst)','there','which','no','yes','smtp','date:','them','said','smtp','from:','to:','net','very','also','org','no','all','there','&nbsp''(cdt)','their','ms','mrs','ll','how','org','one','what','us','those','into','what','more','those','into','because','pp','out','than','many','any','only','some','such','its','these',"new","must",'way','up','ve','again','too','fwd']
    days=['mon','tue','wed','thu','fri','sat','sun']
    months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    stopList=stopList+days+months
    for term in terms:
        if term in stopList:
            continue
        if "\\" in term:
            continue
        if sum(c.isalpha() for c in term) < len(term)/float(2):
            continue
        if term.isdigit():
            continue
        if len(term) > 20:
            continue
        if len(term) == 1:
            continue
        else:
            newTerms.append(term)
    return newTerms
