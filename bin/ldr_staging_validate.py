
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

from uchicagoldrStaging.validation.validateBase import ValidateBase
from uchicagoldrStaging.validation.validateOrganization import ValidateOrganization

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
                         const=INFO,default='WARN' \
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
    parser.add_argument("item", help="Enter the staging root of a staging directory to verify (the ARK directory)"
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
    ch.setLevel('INFO')
    logger.setLevel('DEBUG')
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    #BEGIN MAIN HERE - EXAMPLE BELOW
    try:
        logger.info("Validating Base Structure.")
        validation=ValidateBase(args.item)
        if validation[0] != True:
            logger.critical("Your staging base has not validated!")
            logger.critical(validation)
            exit(1)

        dataPath=join(*validation[1:],'data')
        adminPath=join(*validation[1:],'admin')

        logger.info("Checking data directory.")
        dataValid=ValidateOrganization(dataPath)
        if dataValid[0] != True:
            logger.critical("Your data directory is not well formed!")
            logger.critical(dataValid)
            exit(1)
        for x in dataValid[1]['notDirs']:
            logger.warn("The following appears in the data dir but is not a directory: "+x)

        logger.info("Checking admin directory.")
        topLevelAdminFiles=['fileConversions.txt','record.json']
        adminValid=ValidateOrganization(adminPath,reqTopFiles=['record.json'],reqDirContents=['fixityFromOrigin.txt','fixityOnDisk.txt','log.txt','rsyncFromOrigin.txt'])
        if adminValid[0] != True:
            logger.critical("Your admin directory is not well formed!")
            logger.critical(adminValid)
            exit(1)
        if dataValid[1]['dirs'] != adminValid[1]['dirs']:
            for x in dataValid[1]['dirs']:
                if x not in adminValid[1]['dirs']:
                    logger.warn("Directory appears in data but not admin: "+x)
            for x in adminValid[1]['dirs']:
                if x not in dataValid[1]['dirs']:
                    logger.warn("Directory appears in admin but not data: "+x)
        logger.info('Run complete')
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
