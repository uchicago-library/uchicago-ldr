
__author__ = "Brian Balsamo"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "0.0.1"
__maintainer__ = "Brian Balsamo"
__email__ = "balsamo@uchicago.edu"
__status__ = "Development"

"""
A quick simple script for making a staging structure in a given root
"""

from argparse import ArgumentParser
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit
from os.path import exists,join

from bash_cmd import BashCommand

def main():
    # start of parser boilerplate
    parser = ArgumentParser(description="A small python utility for making an LDR appropriate staging structure",
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
    parser.add_argument("root",help="Enter the root of the staging directory path",
                        action="store"
    )
    parser.add_argument("ark",help="Enter the ark of placeholder",
                        action="store"
    )
    parser.add_argument("ead",help="Enter the EADID suffix",
                        action="store"
    )
    parser.add_argument("accno",help="Enter the accession number",
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
    try:
        root=args.root
        ark=args.ark
        ead=args.ead
        accno=args.accno
        assert(exists(root))
        mkAdminDirArgs=['mkdir','-p',join(root,ark,ead,accno,"admin")]
        mkAdminDirCommand=BashCommand(mkAdminDirArgs)
        assert(mkAdminDirCommand.run_command()[0])
        assert(mkAdminDirCommand.get_data()[1].returncode == 0)
        mkDataDirArgs=['mkdir',join(root,ark,ead,accno,"data")]
        mkDataDirCommand=BashCommand(mkDataDirArgs)
        assert(mkDataDirCommand.run_command()[0])
        assert(mkDataDirCommand.get_data()[1].returncode == 0)
        print("New staging root is:\n"+join(root,ark))
            
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
