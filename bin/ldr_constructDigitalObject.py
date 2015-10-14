
__author__ = "Tyler Danstrom"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "0.0.1"
__maintainer__ = "Tyler Danstrom"
__email__ = "tdanstrom@uchicago.edu"
__status__ = "Prototype"
__description__ = "This is a program for creating digital objects to " + \
                  "conform with a defined specification"

from sys import argv, path

from argparse import ArgumentParser
from hashlib import md5
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit

def main():
    parser = ArgumentParser(description="{description}". \
                            format(description = __description__),
                            epilog="{copyright}; ". \
                            format(copyright = __copyright__) + \
                            "written by {author} <{email}>.". \
                            format(author = __author__,
                                   email = __email__)) 
    parser.add_argument("-v", help="See the version of this program",
                        action="version", version=__version__)
    parser.add_argument( \
                         '-b','-verbose',help="set verbose logging",
                         action='store_const',dest='log_level',
                         const=INFO \
    )
    parser.add_argument( \
                         '-d','--debugging',help="set debugging logging",
                         action='store_const',dest='log_level',
                         const=DEBUG \
    ) 
    parser.add_argument( \
                         '-l','--log_loc',help="save logging to a file",
                         action="store_const",dest="log_loc",
                         const='./{progname}.log'. \
                         format(progname=argv[0]) \
    )
    parser.add_argument( \
                         "-" \
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
    try:
        logger.setLevel(args.log_level)
    except TypeError:
        logger.setLevel(INFO)
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    try:
        
        logger.info("This is a template program.")
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
