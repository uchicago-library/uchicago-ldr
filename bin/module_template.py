
__author__ = "[name]"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = ").0.0"
__maintainer__ = "[name]"
__email__ = "[email]"
__status__ = "[Prototype/Development/Production/etc]"

"""
[A brief description of the module as a whole]
"""


### Default package imports begin ###
from argparse import ArgumentParser
from os import _exit
from os.path import split,exists
### Default package imports end ###

### Third party package imports begin ###
### Third party package imports end ###

### Local package imports begin ###
from uchicagoldrLogging.masterLogger import MasterLogger
from uchicagoldrLogging.handlers import DefaultTermHandler,DebugTermHandler,DefaultFileHandler,DebugFileHandler,DefaultTermHandlerAtLevel,DefaultFileHandlerAtLevel

from uchicagoldr.batch import Batch
from uchicagoldr.item import Item
### Local package imports end ###


### Functions begin ###
### Functions end ###


def main():
    ### Master log instantiation begins ###
    global masterLog
    masterLog=MasterLogger()
    ### Master log instantiation ends ###

    ### Application specific log instantation begins ###
    global logger
    logger=masterLog.getChild('app')
    termHandler=DefaultTermHandler()
    logger.addHandler(termHandler)
    ### Application specific log instantation ends ###

    ### Parser instantiation begins ###
    parser = ArgumentParser(description="[A brief description of the utility]",
                            epilog="Copyright University of Chicago; " + \
                            "written by "+__author__ + \
                            " "+__email__)

    parser.add_argument("-v", help="See the version of this program",
                        action="version", version=__version__)
    # let the user decide the verbosity level of logging statements
    # -b sets it to INFO so warnings, errors and generic informative statements
    # will be logged
    parser.add_argument( \
                         '-b','--verbosity',help="set logging verbosity (DEBUG,INFO,WARN,ERROR,CRITICAL)",
                         nargs='?',
                         const='INFO' \
    )
    # -d is debugging so anything you want to use a debugger gets logged if you
    # use this level
    parser.add_argument( \
                         '-d','--debugging',help="set debugging logging",
                         action='store_true' \
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

    ### Begin argument post processing, if required ###
    if args.verbosity and args.verbosity not in ['DEBUG','INFO','WARN','ERROR','CRITICAL']:
        logger.error("You did not pass a valid argument to the verbosity flag! Valid arguments include: 'DEBUG','INFO','WARN','ERROR', and 'CRITICAL'")
        return(1)
    if args.log_loc:
        if not exists(split(args.log_loc)[0]):
            logger.error("The specified log location does not exist!")
            return(1)
    ### End argument post processing ###

    ### Begin user specified log instantiation, if required ###
    if args.log_loc:
        fileHandler=DefaultFileHandler(args.log_loc)
        logger.addHandler(fileHandler)

    if args.verbosity:
        logger.removeHandler(termHandler)
        termHandler=DefaultTermHandlerAtLevel(args.verbosity)
        logger.addHandler(termHandler)
        if args.log_loc:
            logger.removeHandler(fileHandler)
            fileHandler=DefaultFileHandlerAtLevel(args.log_loc,args.verbosity)
            logger.addHandler(fileHandler)

    if args.debugging:
        logger.removeHandler(termHandler)
        termHandler=DebugTermHandler()
        logger.addHandler(termHandler)
        if args.log_loc:
            logger.removeHandler(fileHandler)
            fileHandler=DebugFileHandler(args.log_loc)
            logger.addHandler(fileHandler)
    ### End user specific log instantiation
    try:
        ### Begin module code ###
        b = Batch(args.root, args.item)
        for item in b.find_items(from_directory=True):
            print(item.get_file_path())
            
        return 0
        ### End module code ###
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
