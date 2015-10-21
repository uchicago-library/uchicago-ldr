
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
from operator import itemgetter

from uchicagoldr.batch import Batch
from uchicagoldr.item import Item
from uchicagoldr.textdocument import TextDocument
from uchicagoldr.textbatch import TextBatch
from uchicagoldr.textprocessingfunctions import pruneTerms

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
    parser.add_argument("restritem", help="Enter a noid for an accession or a " + \
                        "directory path that you need to validate against" + \
                        " a type of controlled collection"
    )
    parser.add_argument("restrroot",help="Enter the root of the directory path",
                        action="store"
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
        b = Batch(args.restrroot, args.restritem)
        textDocs=TextBatch(args.restritem,args.restrroot)
        for item in b.find_items(from_directory=True):
            if ".presform.txt" in item.find_file_name():
                textDoc=TextDocument(item.get_file_path(),item.get_root_path())
                textDocs.add_item(textDoc)
        if textDocs.validate_items():
            logger.info("Beep boop computing TFIDFs")
            logger.info("Finding terms")
            textDocs.set_terms(pruneTerms(textDocs.find_terms()))
            logger.info("Finding unique terms")
            textDocs.set_unique_terms(textDocs.find_unique_terms())
            logger.info("Finding term counts")
            textDocs.set_term_counts(textDocs.find_term_counts())
            logger.info("Finding doc counts")
            textDocs.set_doc_counts(textDocs.find_doc_counts())
            textDocs.set_idfs(textDocs.find_idfs())
            logger.info("Finding TFIDFs")
            textDocs.set_batch_tf_idfs(textDocs.find_batch_tf_idfs())
            logger.info("Generating restrictions VSM")
            textDocs.set_vector_space_model(textDocs.find_vector_space_model())
            restrictionsVSM=textDocs.get_vector_space_model()
        
        checkb = Batch(args.root,args.item)
        sims=[]
        checkTextBatch=TextBatch(args.item,args.root)
        for item in checkb.find_items(from_directory=True):
            if ".presform.txt" in item.find_file_name():
                textDoc=TextDocument(item.get_file_path(),item.get_root_path(),in_batch=checkTextBatch)
                checkTextBatch.add_item(textDoc)
        if checkTextBatch.validate_items():
            checkTextBatch.set_terms(pruneTerms(checkTextBatch.find_terms()))
            checkTextBatch.set_unique_terms(checkTextBatch.find_unique_terms())
            checkTextBatch.set_doc_counts(checkTextBatch.find_doc_counts())
            #checkTextBatch.set_idfs(checkTextBatch.find_idfs())
            mockIDFS={}
            for term in checkTextBatch.get_terms():
                mockIDFS[term]=1
            checkTextBatch.set_idfs(mockIDFS)
            checkTextBatch.set_item_tf_idfs(checkTextBatch.find_item_tf_idfs())
            rels={}
            for item in checkTextBatch:
                item.set_tf_idfs(item.find_tf_idfs())
                item.set_vector_space_model(item.find_vector_space_model())
                path=item.get_file_path()
                rel=textDocs.find_similarity(item.get_vector_space_model())
                rels[path]=rel
            sortedrels = sorted(rels.items(), key=itemgetter(1))
            first10=sortedrels[0:10]
            for thing in sortedrels:
                print(thing)
            
            
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
