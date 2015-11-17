
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

def getImmediateSubDirs(path):
    return [name for name in listdir(path) if isdir(join(path,name))]

def main():
    log_format = Formatter( \
                            "[%(levelname)s] %(asctime)s  " + \
                            "= %(message)s",
                            datefmt="%Y-%m-%dT%H:%M:%S" \
    )
    global logger
    logger = getLogger( \
                        "lib.uchicago.repository.logger" \
    )
    logger.setLevel('DEBUG')
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
    parser.add_argument("item", help="Enter a noid for an accession or a " + \
                        "directory path that you need to validate against" + \
                        " a type of controlled collection"
    )
    parser.add_argument("root",help="Enter the root of the directory path",
                        action="store"
    )
    parser.add_argument("dest_root",help="Enter the destination root path",
                        action='store'
    )
    parser.add_argument("prefix",help="The prefix of the containing folder on disk",
                        action='store'
    )
    parser.add_argument("--rehash",help="Disregard any existing previously generated hashes, recreate them on this run",
                        action="store_true"
    )
    parser.add_argument("--chain",help="Write the prefix+num to stdout, for chaining this command into the others via some intermediate connection",
                        action="store_true"
    )
    parser.add_argument("--weird-root",help="If for some reason you deliberately want to generate a strange item root structure which doesn't reflect rsyncs path interpretation behavior pass this option",default=False,
                        action="store_true"
    )
    args = parser.parse_args()
    ch = StreamHandler()
    ch.setFormatter(log_format)
    ch.setLevel(args.log_level)
    logger.addHandler(ch)
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    if args.item[-1] == "/" and args.item != args.root and not args.weird_root:
        logger.critical("Root appears to not conform to rsync path specs.")
        exit(1)
    try:
        assert(isdir(args.dest_root))
        shouldBeEAD=getImmediateSubDirs(args.dest_root)
        assert(len(shouldBeEAD)==1)
        shouldBeAccNo=getImmediateSubDirs(join(args.dest_root,shouldBeEAD[0]))
        assert(len(shouldBeAccNo)==1)
        stageRoot=join(join(args.dest_root,shouldBeEAD[0]),shouldBeAccNo[0])
        destinationAdminRoot=join(stageRoot,'admin/')
        destinationDataRoot=join(stageRoot,'data/')
        prefix=args.prefix

        if not prefix[-1].isdigit():

            existingDataSubDirs=[name for name in getImmediateSubDirs(destinationDataRoot) if prefix in name]

            if len(existingDataSubDirs) < 1:
                nextNum=str(1)
            else:
                nums=[]
                for directory in existingDataSubDirs:
                    num=directory.strip(prefix)
                    nums.append(int(num))
                nums.sort()
                nextNum=str(nums[-1]+1)
            logger.info("Creating new data and admin directories for your prefix: "+prefix+nextNum)

            destinationAdminFolder=join(destinationAdminRoot,prefix+nextNum)
            destinationDataFolder=join(destinationDataRoot,prefix+nextNum)

            mkAdminDirArgs=['mkdir',destinationAdminFolder]
            mkAdminDirComm=BashCommand(mkAdminDirArgs)
            assert(mkAdminDirComm.run_command()[0])
            logger.debug("mkAdminDir output begins")
            logger.debug(mkAdminDirComm.get_data()[1].args)
            logger.debug(mkAdminDirComm.get_data()[1].returncode)
            logger.debug(mkAdminDirComm.get_data()[1].stdout)
            logger.debug("mkAdminDir output ends")

            mkDataDirArgs=['mkdir',destinationDataFolder]
            mkDataDirComm=BashCommand(mkDataDirArgs)
            assert(mkDataDirComm.run_command()[0])
            logger.debug("mkDataDir output begins")
            logger.debug(mkDataDirComm.get_data()[1].args)
            logger.debug(mkDataDirComm.get_data()[1].returncode)
            logger.debug(mkDataDirComm.get_data()[1].stdout)
            logger.debug("mkAdminDir output ends")

            assert(isdir(destinationAdminFolder))
            assert(isdir(destinationDataFolder))

        else:
            logger.info("Attempting to resume transfer into "+join(destinationDataRoot,prefix))
            nextNum=""
            
            destinationAdminFolder=join(destinationAdminRoot,prefix)
            assert(isdir(destinationAdminFolder))
            destinationDataFolder=join(destinationDataRoot,prefix)
            assert(isdir(destinationDataFolder))

        stagingDebugLog = FileHandler(join(destinationAdminFolder,'log.txt'))
        stagingDebugLog.setFormatter(log_format)
        stagingDebugLog.setLevel('DEBUG')
        logger.addHandler(stagingDebugLog)

        logger.info("Beginning rsync")
        rsyncArgs=['rsync','-avz',args.item,destinationDataFolder]
        rsyncCommand=BashCommand(rsyncArgs)
        assert(rsyncCommand.run_command()[0])
        with open(join(destinationAdminFolder,'rsyncFromOrigin.txt'),'a') as f:
            f.write(str(rsyncCommand.get_data()[1])+'\n')
        if rsyncCommand.get_data()[1].returncode != 0:
            logger.warn("Rsync exited with a non-zero return code: "+str(rsyncCommand.get_data()[1].returncode))
        logger.debug("Rsync output begins")
        logger.debug(rsyncCommand.get_data()[1].args)
        logger.debug(rsyncCommand.get_data()[1].returncode)
        for line in rsyncCommand.get_data()[1].stdout.split('\n'):
            logger.debug(line)
        logger.debug("Rsync output ends")
        logger.info("Rsync complete.")

        if args.chain:
            logger.info(prefix+nextNum)

        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
