
__author__ = "Brian Balsamo"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "0.0.1"
__maintainer__ = "Brian Balsamo"
__email__ = "Balsamo@uchicago.edu"
__status__ = "Development"

"""
A small utility for validating staging structures after they have been populated, alerting the user to any potential errors
"""

from argparse import ArgumentParser
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit,listdir
from os.path import relpath,join,isdir,isfile
from re import compile as re_compile

from uchicagoldr.batch import Batch
from uchicagoldr.item import Item

def main():
    # start of parser boilerplate
    parser = ArgumentParser(description="A utility for validating staging structures after they have been populated, meant to alert the user to any potential errors",
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
    #BEGIN MAIN HERE - EXAMPLE BELOW
    try:
#        pathNoRoot=relpath(args.item,start=args.root)
        logger.info("Checking the ARK.")
        ark=relpath(args.item,start=args.root)
        if not re_compile('\w{13}').match(ark):
            logger.warn(ark+" doesn't look like a valid ARK!"

        logger.info("Checking ARK directory")
        if len(listdir(args.item)) > 1:
            logger.warn("It appears as though there is more than one thing in the ARK directory!")
            logger.warn("Directory contents: "+listdir(args.item))

        eadSuffix=listdir(args.item)[1]
        eadPath=join(args.item,eadSuffix)
        if eadSuffix != eadSuffix.upper():
            logger.warn("Your EAD suffix isn't capitalized!")
            logger.warn("EAD Suffix: "+eadSuffix)

        if len(listdir(eadPath)) > 1:
            logger.warn("It appears as though there is more than one thing in your EAD directory!")


        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
