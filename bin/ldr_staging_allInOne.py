
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
        pythonPath='python3'
        scriptsLoc='/Users/balsamo/repos/uchicago-ldr/bin/'

        mvArgs=[pythonPath,scriptsLoc+'ldr_staging_moveFiles.py',args.item,args.root,args.dest_root,args.prefix,"--chain"]
        mvCommand=BashCommand(mvArgs)
        assert(mvCommand.run_command()[0])
        print("\n".join(mvCommand.get_data()[1].stdout.split('\n')))
        folder=mvCommand.get_data()[1].stdout.split('=')[-1].rstrip('\n').strip()

        origHashArgs=[pythonPath,scriptsLoc+'ldr_staging_originHash.py',args.item,args.root,args.dest_root,folder]
        if args.rehash:
            origHashArgs.append("--rehash")
        origHashCommand=BashCommand(origHashArgs)
        assert(origHashCommand.run_command()[0])
        print("\n".join(origHashCommand.get_data()[1].stdout.split('\n')))

        stageHashArgs=[pythonPath,scriptsLoc+'ldr_staging_stagingHash.py',args.dest_root,folder]
        if args.rehash:
            stageHashArgs.append("--rehash")
        stageHashCommand=BashCommand(stageHashArgs)
        assert(stageHashCommand.run_command()[0])
        print("\n".join(stageHashCommand.get_data()[1].stdout.split('\n')))

        auditArgs=[pythonPath,scriptsLoc+'ldr_staging_audit.py',args.dest_root,folder]
        auditCommand=BashCommand(auditArgs)
        assert(auditCommand.run_command()[0])
        print("\n".join(auditCommand.get_data()[1].stdout.split('\n')))
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
