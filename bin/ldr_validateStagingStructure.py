
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
    logger.setLevel(args.log_level)
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    #BEGIN MAIN HERE - EXAMPLE BELOW
    try:
        logger.info("Checking the ARK.")
        if not isdir(args.item):
            logger.warn("The provided staging root isn't a directory!")
            return 1
        ark=relpath(args.item,start=args.root)
        if not re_compile('^\w{13}$').match(ark):
            logger.warn(ark+" doesn't look like a valid ARK!")

        logger.info("Checking ARK directory")
        if len(listdir(args.item)) > 1:
            logger.warn("It appears as though there is more than one thing in the ARK directory!")
            logger.warn("Directory contents: "+",".join(listdir(args.item)))
            return 1

        logger.info("Checking the EAD ID.")
        eadSuffix=listdir(args.item)[0]
        eadPath=join(args.item,eadSuffix)
        if eadSuffix != eadSuffix.upper():
            logger.warn("Your EAD suffix isn't capitalized!")
            logger.warn("EAD Suffix: "+eadSuffix)

        logger.info("Checking the EAD ID Directory.")
        if not isdir(eadPath):
            logger.warn("The EADID isn't a directory!")
            return 1
        if len(listdir(eadPath)) > 1:
            logger.warn("It appears as though there is more than one thing in your EAD directory!")
            logger.warn("Directory contents: "+",".join(listdir(eadPath)))
            return 1

        accNo=listdir(eadPath)[0]
        accNoPath=join(eadPath,accNo)

        logger.info("Checking the accession number")
        pattern=re_compile('^\d{4}-\d{3}$')
        if not pattern.match(accNo):
            logger.warn('Your accession number doesn\'t appear to be valid.')
            loggern.warn('Accession Number: '+accNo)

        logger.info("Checking the accession number directory.")
        if not isdir(eadPath):
            logger.warn("The accession number isn't a directory!")
            return 1
        if len(listdir(accNoPath)) != 2 or 'data' not in listdir(accNoPath) or 'admin' not in listdir(accNoPath):
            if len(listdir(accNoPath)) != 2:
                logger.warn("There appear to be too many or too few directories in your accession number directory.")
            if 'data' not in listdir(accNoPath):
                logger.warn("There doesn't appear to be a data directory in your accession number directory.")
                return 1
            if 'admin' not in listdir(accNoPath):
                logger.warn("There doesn't appear to be an admin directory in your accession number directory.")
                return 1
            logger.warn('Accession number directory contents: '+",".join(listdir(accNoPath)))

        logger.info("Checking data directory.")
        dataPath=join(accNoPath,"data")
        if not isdir(dataPath):
            logger.warn("The data path isn't a directory!")
            return 1
        dataFolderList=listdir(dataPath)
        prefixList=[]
        for folder in dataFolderList:
            if not isdir(join(dataPath,folder)):
                logger.warn(join(dataPath,folder)+" isn't a directory!")
            prefix=re_compile('^[a-zA-Z_-]*').match(folder).group(0)
            try:
                prefix=re_compile('^[a-zA-Z_-]*').match(folder).group(1)
                logger.warn("Your prefix appears to have more letters after its index!")
            except IndexError:
                pass
            prefixList.append(prefix)
        prefixList=set(prefixList)
        logger.info('Prefixes include: '+str(prefixList))
        for prefix in prefixList:
            prefixSet=[directory for directory in listdir(dataPath) if re_compile('^'+prefix).match(directory)]
            nums=[]
            for folder in prefixSet:
                num=folder.lstrip(prefix)
                nums.append(int(num))
            maxNum=max(nums)
            for i in range(1,maxNum+1):
                if i not in nums:
                    logger.warn("You appear to be missing a folder!")
                    logger.warn("Missing folder in data directory: "+prefix+str(i))

        logger.info("Checking admin directory.")
        adminPath=join(accNoPath,"admin")
        adminFolderList=listdir(adminPath)
        adminPrefixList=[]
        for folder in adminFolderList:
            if not isdir(join(adminPath,folder)):
                logger.warn(join(adminPath,folder)+" isn't a directory!")
                return 1
            prefix=re_compile('^[a-zA-Z_-]*').match(folder).group(0)
            try:
                prefix=re_compile('^[a-zA-Z_-]*').match(folder).group(1)
                logger.warn("Your prefix appears to have more letters after its index!")
            except IndexError:
                pass
            adminPrefixList.append(prefix)
        adminPrefixList=set(adminPrefixList)
        for prefix in adminPrefixList:
            if prefix not in prefixList:
                logger.warn("The '"+prefix+"' prefix appears in the admin directory but not the data directory!")
        for prefix in prefixList:
            if prefix not in adminPrefixList:
                logger.warn("The '"+prefix+"'prefix appears in the data directory but not the admin directory!")
        for prefix in adminPrefixList:
            prefixSet=[directory for directory in listdir(adminPath) if re_compile('^'+prefix).match(directory)]
            nums=[]
            for folder in prefixSet:
                num=folder.lstrip(prefix)
                nums.append(int(num))
            maxNum=max(nums)
            for i in range(1,maxNum+1):
                if i not in nums:
                    logger.warn("You appear to be missing a folder!")
                    logger.warn("Missing folder in admin directory: "+prefix+str(i))
        for folder in adminFolderList:
            adminFolderPath=join(adminPath,folder)
            for recAdminData in ['fixityFromOrigin.txt','fixityInStaging.txt','log.txt','rsyncFromOrigin.txt']:
                if recAdminData not in listdir(adminFolderPath) or not isfile(join(adminFolderPath,recAdminData)):
                    logger.warn("You appear to be missing a staging administrative component!")
                    logger.warn(recAdminData+" missing from: "+adminFolderPath)
        for folder in adminFolderList:
            if folder not in dataFolderList:
                logger.warn("You have a folder in your admin folder that is not in your data folder!")
                logger.warn(join(adminPath,folder)+" appears in admin but not in data.")
        for folder in dataFolderList:
            if folder not in adminFolderList:
                logger.warn("You have a folder in your data folder that is not in your admin folder!")
                logger.warn(join(dataPath,folder)+" appears in data but not in admin.")



        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
