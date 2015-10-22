
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
from hashlib import md5
from hashlib import sha256

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
    parser.add_argument("dest_root",help="Enter the destination root path",
                        action='store'
    )
    parser.add_argument("prefix",help="The prefix of the containing folder on disk",
                        action='store'
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
        shouldBeEAD=getImmediateSubDirs(args.dest_root)
        assert(len(shouldBeEAD)==1)
        shouldBeAccNo=getImmediateSubDirs(join(args.dest_root,shouldBeEAD[0]))
        assert(len(shouldBeAccNo)==1)
        stageRoot=join(join(args.dest_root,shouldBeEAD[0]),shouldBeAccNo[0])
        destinationAdminRoot=join(stageRoot,'admin/')
        destinationDataRoot=join(stageRoot,'data/')
        prefix=args.prefix

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

        mkAdminDirArgs=['mkdir',destinationAdminRoot+prefix+nextNum]
        mkAdminDirComm=BashCommand(mkAdminDirArgs)
        assert(mkAdminDirComm.run_command()[0])
        logger.info("mkAdminDir output begins")
        logger.info(mkAdminDirComm.get_data()[1].args)
        logger.info(mkAdminDirComm.get_data()[1].returncode)
        logger.info(mkAdminDirComm.get_data()[1].stdout)
        logger.info("mkAdminDir output ends")

        mkDataDirArgs=['mkdir',destinationDataRoot+prefix+nextNum]
        mkDataDirComm=BashCommand(mkDataDirArgs)
        assert(mkDataDirComm.run_command()[0])
        logger.info("mkDataDir output begins")
        logger.info(mkDataDirComm.get_data()[1].args)
        logger.info(mkDataDirComm.get_data()[1].returncode)
        logger.info(mkDataDirComm.get_data()[1].stdout)
        logger.info("mkAdminDir output ends")

        logger.info("Beginning rsync")
        rsyncArgs=['rsync','-avz',args.item,destinationDataRoot+prefix+nextNum]
        rsyncCommand=BashCommand(rsyncArgs)
        assert(rsyncCommand.run_command()[0])
        logger.info("Rsync output begins")
        logger.info(rsyncCommand.get_data()[1].args)
        logger.info(rsyncCommand.get_data()[1].returncode)
        for line in rsyncCommand.get_data()[1].stdout.split(b'\n'):
            logger.info(line)
        logger.info("Rsync output ends")

        logger.info("Creating batch from original files.")
        originalFiles=Batch(args.root,directory=args.item)

        originalFileHashes={}
        logger.info("Hashing original files")
        for item in originalFiles.find_items(from_directory=True):
            item.set_sha256(item.find_sha256_hash())
            item.set_md5(item.find_md5_hash())
            originalFileHashes[relpath(item.get_file_path(),start=item.get_root_path())]=[item.get_sha256(),item.get_md5()]

        logger.info("Creating batch from moved files.")
        movedFiles=Batch(args.dest_root,directory=destinationDataRoot)
        
        movedFileHashes={}
        logger.info("Hashing copied files.")
        for item in movedFiles.find_items(from_directory=True):
            item.set_sha256(item.find_sha256_hash())
            item.set_md5(item.find_md5_hash())
            movedFileHashes[relpath(item.get_file_path(),start=join(destinationDataRoot,prefix+nextNum))]=[item.get_sha256(),item.get_md5()]

        notMoved=[key for key in originalFileHashes.keys() if key not in movedFileHashes.keys()]
        badHash=[key for key in originalFileHashes.keys() if key not in notMoved and originalFileHashes[key] != movedFileHashes[key]]


        for entry in originalFileHashes:
            if entry not in notMoved and entry not in badHash:
                logger.info("GOOD: "+entry+":"+str(originalFileHashes[entry]))
            elif entry in notMoved:
                logger.info("NOT MOVED: "+entry+":"+str(originalFileHashes[entry]))
            elif entry in badHash:
                logger.info("BAD HASH: "+entry+":"+str(originalFileHashes[entry]))
       
        logger.info(str(len(originalFileHashes)-len(notMoved)-len(badHash))+" files moved without issue.")
        logger.info(str(len(notMoved))+" files not copied.")
        logger.info(str(len(badHash))+" have a different hash from the origin.")

        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
