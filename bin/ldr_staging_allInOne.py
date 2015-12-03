#!/usr/bin/python3

# Default package imports begin #
from argparse import ArgumentParser
from os import _exit
from os.path import split, exists, dirname, realpath
from re import match
# Default package imports end #

# Third party package imports begin #
# Third party package imports end #

# Local package imports begin #
from uchicagoldrLogging.loggers import MasterLogger
from uchicagoldrLogging.handlers import DefaultTermHandler, DebugTermHandler, \
    DefaultFileHandler, DebugFileHandler, DefaultTermHandlerAtLevel,\
    DefaultFileHandlerAtLevel
from uchicagoldrLogging.filters import UserAndIPFilter

from uchicagoldr.bash_cmd import BashCommand
# Local package imports end #

# Header info begins #
__author__ = "Brian Balsamo"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "0.0.1"
__maintainer__ = "Brian Balsamo"
__email__ = "balsamo@uchicago.edu"
__status__ = "Development"
# Header info ends #

"""
This module is meant to take a location on physical media (or all the contents)
 and move it into disk space in the LDR staging area.
"""

# Functions begin #
# Functions end #


def main():
    # Master log instantiation begins #
    global masterLog
    masterLog = MasterLogger()
    # Master log instantiation ends #

    # Application specific log instantation begins #
    global logger
    logger = masterLog.getChild(__name__)
    f = UserAndIPFilter()
    termHandler = DefaultTermHandler()
    logger.addHandler(termHandler)
    logger.addFilter(f)
    logger.info("BEGINS")
    # Application specific log instantation ends #

    # Parser instantiation begins #
    parser = ArgumentParser(description="[A brief description of the utility]",
                            epilog="Copyright University of Chicago; " +
                            "written by "+__author__ +
                            " "+__email__)

    parser.add_argument(
                        "-v",
                        help="See the version of this program",
                        action="version",
                        version=__version__
    )
    # let the user decide the verbosity level of logging statements
    # -b sets it to INFO so warnings, errors and generic informative statements
    # will be logged
    parser.add_argument(
                        '-b', '--verbosity',
                        help="set logging verbosity " +
                        "(DEBUG,INFO,WARN,ERROR,CRITICAL)",
                        nargs='?',
                        const='INFO'
    )
    # -d is debugging so anything you want to use a debugger gets logged if you
    # use this level
    parser.add_argument(
                        '-d', '--debugging',
                        help="set debugging logging",
                        action='store_true'
    )
    # optionally save the log to a file.
    # Set a location or use the default constant
    parser.add_argument(
                        '-l', '--log_loc',
                        help="save logging to a file",
                        dest="log_loc",

    )
    parser.add_argument(
                        "item",
                        help="Enter a noid for an accession or a " +
                        "directory path that you need to validate against" +
                        " a type of controlled collection"
    )
    parser.add_argument(
                        "root",
                        help="Enter the root of the directory path",
                        action="store"
    )
    parser.add_argument(
                        "dest_root",
                        help="Enter the destination root path",
                        action='store'
    )
    parser.add_argument(
                        "prefix",
                        help="The prefix of the containing folder on disk",
                        action='store'
    )
    parser.add_argument(
                        "--rehash",
                        help="Disregard any existing previously generated" +
                        "hashes, recreate them on this run",
                        action="store_true"
    )
    parser.add_argument(
                        "--scriptloc",
                        help="Specify and alternate script location"
                        action="store"
    )
    try:
        args = parser.parse_args()
    except SystemExit:
        logger.critical("ENDS: Command line argument parsing failed.")
        exit(1)

    # Begin argument post processing, if required #
    if args.verbosity and args.verbosity not in ['DEBUG', 'INFO',
                                                 'WARN', 'ERROR', 'CRITICAL']:
        logger.critical("You did not pass a valid argument to the verbosity \
                        flag! Valid arguments include: \
                        'DEBUG','INFO','WARN','ERROR', and 'CRITICAL'")
        return(1)
    if args.log_loc:
        if not exists(split(args.log_loc)[0]):
            logger.critical("The specified log location does not exist!")
            return(1)
    # End argument post processing #

    # Begin user specified log instantiation, if required #
    if args.log_loc:
        fileHandler = DefaultFileHandler(args.log_loc)
        logger.addHandler(fileHandler)

    if args.verbosity:
        logger.removeHandler(termHandler)
        termHandler = DefaultTermHandlerAtLevel(args.verbosity)
        logger.addHandler(termHandler)
        if args.log_loc:
            logger.removeHandler(fileHandler)
            fileHandler = DefaultFileHandlerAtLevel(args.log_loc,
                                                    args.verbosity)
            logger.addHandler(fileHandler)

    if args.debugging:
        logger.removeHandler(termHandler)
        termHandler = DebugTermHandler()
        logger.addHandler(termHandler)
        if args.log_loc:
            logger.removeHandler(fileHandler)
            fileHandler = DebugFileHandler(args.log_loc)
            logger.addHandler(fileHandler)
    # End user specified log instantiation #
    try:
        # Begin module code #
        pythonPath = 'python3'
        if not args.scriptloc:
            scriptsLoc = dirname(realpath(__file__))
        else:
            scriptsLoc = args.scriptloc

        mvArgs = [pythonPath, scriptsLoc+'ldr_staging_moveFiles.py',
                  args.item, args.root, args.dest_root, args.prefix, "--chain"]
        mvCommand = BashCommand(mvArgs)
        assert(mvCommand.run_command()[0])
        print("\n".join(mvCommand.get_data()[1].stdout.split('\n')))
        for line in mvCommand.get_data()[1].stdout.split('\n'):
            if match('^\[CRITICAL\]', line):
                print("Critical error detected. Exiting")
                exit(1)
        folder = mvCommand.get_data()[1].stdout.split('=')[-1].rstrip('\n').strip()

        origHashArgs = [pythonPath, scriptsLoc+'ldr_staging_originHash.py',
                        args.item, args.root, args.dest_root, folder]
        if args.rehash:
            origHashArgs.append("--rehash")
        origHashCommand = BashCommand(origHashArgs)
        assert(origHashCommand.run_command()[0])
        print("\n".join(origHashCommand.get_data()[1].stdout.split('\n')))
        for line in origHashCommand.get_data()[1].stdout.split('\n'):
            if match('^\[CRITICAL\]', line):
                print("Critical error detected. Exiting")
                exit(1)

        stageHashArgs = [pythonPath, scriptsLoc+'ldr_staging_stagingHash.py',
                         args.dest_root, folder]
        if args.rehash:
            stageHashArgs.append("--rehash")
        stageHashCommand = BashCommand(stageHashArgs)
        assert(stageHashCommand.run_command()[0])
        print("\n".join(stageHashCommand.get_data()[1].stdout.split('\n')))
        for line in stageHashCommand.get_data()[1].stdout.split('\n'):
            if match('^\[CRITICAL\]', line):
                print("Critical error detected. Exiting")
                exit(1)

        auditArgs = [pythonPath, scriptsLoc+'ldr_staging_audit.py',
                     args.dest_root, folder]
        auditCommand = BashCommand(auditArgs)
        assert(auditCommand.run_command()[0])
        print("\n".join(auditCommand.get_data()[1].stdout.split('\n')))
        for line in auditCommand.get_data()[1].stdout.split('\n'):
            if match('^\[CRITICAL\]', line):
                print("Critical error detected. Exiting")
                exit(1)
        # End module code #
        logger.info("ENDS: COMPLETE")
        return 0
    except KeyboardInterrupt:
        logger.error("ENDS: Program aborted manually")
        return 131
    except Exception as e:
        logger.critical("ENDS: Exception ("+str(e)+")")
        return 1
if __name__ == "__main__":
    _exit(main())
