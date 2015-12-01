
__author__ = "Brian Balsamo"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "0.0.1"
__maintainer__ = "Brian Balsamo"
__email__ = "balsamo@uchicago.edu"
__status__ = "Development"

"""
This module is meant to take a location on physical media (or all the contents) and move it into disk space in the LDR staging area.
"""

from argparse import ArgumentParser
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit
from os import listdir
from os.path import isdir
from os.path import join
from os.path import relpath
from os.path import exists

from uchicagoldr.batch import Batch
from uchicagoldr.item import Item
from uchicagoldr.bash_cmd import BashCommand

from uchicagoldrStaging.validation.validateBase import ValidateBase
from uchicagoldrStaging.population.readExistingFixityLog import ReadExistingFixityLog

def main():
    # start of parser boilerplate
    parser = ArgumentParser(description="A command line utility for staging physical media",
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
                         const=DEBUG,default='DEBUG' \
    )
    # optionally save the log to a file. set a location or use the default constant
    parser.add_argument( \
                         '-l','--log_loc',help="save logging to a file",
                         dest="log_loc",
                         \
    )
    parser.add_argument( \
                         '--log_verb',help="Set a separate verbosity for the log written to disk, if desired",
                         dest="log_verb",default=None
                         \
    )
    parser.add_argument("dest_root",help="Enter the destination root path",
                        action='store'
    )
    parser.add_argument("containing_folder",help="The name of the containing folder on disk (prefix+number)",
                        action='store'
    )
    parser.add_argument("--rehash",help="Disregard any existing previously generated hashes, recreate them on this run",
                        action="store_true"
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
    ch.setLevel(args.log_level)
    logger.setLevel('DEBUG')
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    try:
        validation=ValidateBase(args.dest_root)
        if validation[0] != True:
            logger.critical("Your staging root isn't valid!")
            exit(1)
        else:
            stageRoot=join(*validation[1:])
        destinationAdminRoot=join(stageRoot,'admin/')
        destinationDataRoot=join(stageRoot,'data/')
        containing_folder=args.containing_folder
        destinationAdminFolder=join(destinationAdminRoot,containing_folder)

        stagingDebugLog = FileHandler(join(destinationAdminFolder,'log.txt'))
        stagingDebugLog.setFormatter(log_format)
        stagingDebugLog.setLevel('DEBUG')
        logger.addHandler(stagingDebugLog)

        existingOriginalFileHashes=ReadExistingFixityLog(join(destinationAdminFolder,'fixityFromOrigin.txt'))
        existingMovedFileHashes=ReadExistingFixityLog(join(destinationAdminFolder,'fixityOnDisk.txt'))

        notMoved=[key for key in existingOriginalFileHashes if key not in existingMovedFileHashes]
        foreignFiles=[key for key in existingMovedFileHashes if key not in existingOriginalFileHashes]
        badHash=[key for key in existingOriginalFileHashes if key not in notMoved and existingOriginalFileHashes[key] != existingMovedFileHashes[key]]


        for entry in existingOriginalFileHashes:
            if entry not in notMoved and entry not in badHash:
                logger.debug("GOOD: "+entry+":"+str(existingOriginalFileHashes[entry]))
            elif entry in notMoved:
                logger.debug("NOT MOVED: "+entry+":"+str(existingOriginalFileHashes[entry]))
            elif entry in badHash:
                logger.debug("BAD HASH: "+entry+":"+str(existingOriginalFileHashes[entry]))
        for entry in foreignFiles:
            logger.debug("FOREIGN FILE: "+entry)
       
        logger.info(str(len(existingMovedFileHashes))+" file(s) total in the staging area.")
        logger.info(str(len(notMoved))+" file(s) not copied.")
        logger.info(str(len(badHash))+" file(s) have a different hash from the origin.")
        logger.info(str(len(foreignFiles))+" file(s) appear to not have come from the origin.")

        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
