
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
        shouldBeEAD=getImmediateSubDirs(args.dest_root)
        assert(len(shouldBeEAD)==1)
        shouldBeAccNo=getImmediateSubDirs(join(args.dest_root,shouldBeEAD[0]))
        assert(len(shouldBeAccNo)==1)
        stageRoot=join(join(args.dest_root,shouldBeEAD[0]),shouldBeAccNo[0])
        destinationAdminRoot=join(stageRoot,'admin/')
        destinationDataRoot=join(stageRoot,'data/')
        containing_folder=args.containing_folder
        destinationAdminFolder=join(destinationAdminRoot,containing_folder)
        destinationDataFolder=join(destinationDataRoot,containing_folder)

        stagingDebugLog = FileHandler(join(destinationAdminFolder,'log.txt'))
        stagingDebugLog.setFormatter(log_format)
        stagingDebugLog.setLevel('DEBUG')
        logger.addHandler(stagingDebugLog)

        logger.debug("Creating batch from moved files.")
        movedFiles=Batch(args.dest_root,directory=destinationDataFolder)
        
        existingMovedFileHashes={}
        movedFileHashes={}
        logger.info("Hashing copied files.")
        if exists(join(destinationAdminFolder,'fixityInStaging.txt')):
            with open(join(destinationAdminFolder,'fixityInStaging.txt'),'r') as f:
                if not args.rehash:
                    for line in f.readlines():
                        splitLine=line.split('\t')
                        if splitLine[1] != "ERROR":
                            existingMovedFileHashes[splitLine[0]]=[splitLine[1],splitLine[2].rstrip('\n')]
        with open(join(destinationAdminFolder,'fixityInStaging.txt'),'a') as f:
            for item in movedFiles.find_items(from_directory=True):
                if item.test_readability():
                    item.set_root_path(destinationDataFolder)
                    if relpath(item.get_file_path(),start=item.get_root_path()) not in existingMovedFileHashes:
                        item.set_sha256(item.find_sha256_hash())
                        item.set_md5(item.find_md5_hash())
                        movedFileHashes[relpath(item.get_file_path(),start=destinationDataFolder)]=[item.get_sha256(),item.get_md5()]
                else:
                    logger.warn("COULD NOT READ FILE: "+item.get_file_path())
                    movedFileHashes[relpath(item.get_file_path(),start=destinationDataFolder)]=["ERROR","ERROR"]
            for entry in movedFileHashes:
                f.write(entry+"\t"+movedFileHashes[entry][0]+'\t'+movedFileHashes[entry][1]+'\n')
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
