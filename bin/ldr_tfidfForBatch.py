
__author__ = "Brian Balsamo"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "1.0.0"
__maintainer__ = "Brian Balsamo"
__email__ = "balsamo@uchicago.edu"
__status__ = "Prototype"

"""
Compute the TFIDFs of the terms in .presform.txt files in a batch
"""

from argparse import ArgumentParser
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit

from uchicagoldr.batch import Batch
from uchicagoldr.item import Item
from uchicagoldr.textdocument import TextDocument
from uchicagoldr.textbatch import TextBatch

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

def main():
    # start of parser boilerplate
    parser = ArgumentParser(description="Produce TFIDF numbers for terms in the text preservation formats in a batch",
                            epilog="Copyright University of Chicago; " + \
                            "written by "+__author__ + \
                            " "+__email__)

    parser.add_argument("-v", help="See the version of this program",
                        action="version", version=__version__)
    # let the user decide the verbosity level of logging statements
    # -b sets it to INFO so warnings, errors and generic informative statements
    # will be logged
    parser.add_argument( \
                         '-b','-verbose',help="set verbose logging",
                         action='store_const',dest='log_level',
                         const=INFO,default='INFO' \
    )
    # -d is debugging so anything you want to use a debugger gets logged if you
    # use this level
    parser.add_argument( \
                         '-d','--debugging',help="set debugging logging",
                         action='store_const',dest='log_level',
                         const=DEBUG,default='INFO' \
    )
    # optionally save the log to a file. set a location or use the default constant
    parser.add_argument( \
                         '-l','--log_loc',help="save logging to a file",
                         dest="log_loc",
                         \
    )
    parser.add_argument("item", help="Enter a noid for an accession or a " + \
                        "directory path that you need to validate against" + \
                        " a type of controlled collection"
    )
    parser.add_argument("root",help="Enter the root of the directory path",
                        action="store"
    )
    args = parser.parse_args()
    log_format = Formatter( \
                            "[%(levelname)s] %(asctime)s  " + \
                            "= %(message)s",
                            datefmt="%Y-%m-%dT%H:%M:%S" \
    )
    global logger
    logger = getLogger( \
                        "lib.uchicago.repository.logger" \
    )
    ch = StreamHandler()
    ch.setFormatter(log_format)
    logger.setLevel(args.log_level)
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    try:
        b = Batch(args.root, args.item)
        textDocs=TextBatch(args.item,args.root)
        for item in b.find_items(from_directory=True):
            if ".presform.txt" in item.find_file_name():
                textDoc=TextDocument(item.get_file_path(),item.get_root_path())
                textDocs.add_item(textDoc)
        if textDocs.validate_items():
            logger.info("Finding terms")
            textDocs.set_terms(pruneTerms(textDocs.find_terms()))
            logger.info("Getting unique terms")
            textDocs.set_unique_terms(textDocs.find_unique_terms())
            logger.info("Getting doc counts")
            textDocs.set_doc_counts(textDocs.find_doc_counts())
            logger.info("Beep boop computing TFIDFs")
            for item in textDocs.get_items():
                item.set_terms(pruneTerms(item.find_terms()))
                item.set_term_counts(item.find_term_counts())
                tfidfs=[]
                for term in item.get_term_counts():
                   tfidfs.append((term[0],term[1]/float(textDocs.get_doc_counts()[term[0]])))
                numToPrint=5
                firstX=sorted(tfidfs,key=lambda tup: tup[1],reverse=True)[0:numToPrint-1]
                print(item.get_file_path()+"\n"+str(firstX)+"\n")
                
            
#            terms=item.find_terms()
#            terms=pruneTerms(terms)
#            print(item.find_file_name()+str(terms[0:5]))
            
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
