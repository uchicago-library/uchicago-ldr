
__author__ = "Brian Balsamo"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "0.0.1"
__maintainer__ = "Brian Balsamo"
__email__ = "balsamo@uchicago.edu"
__status__ = "Prototype"

"""
A module meant to ingest a digital acquisitions form and a staged directory and produce a record designed for use by Special Collections and the DAS.
"""

from argparse import ArgumentParser
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit
import json

from uchicagoldr.batch import Batch
from uchicagoldr.item import Item
from uchicagoldr.forms.recordFields import RecordFields
from uchicagoldr.forms.digitalAcquisitionRead import ReadAcquisitionRecord
from uchicagoldr.forms.digitalAcquisitionMap import AcquisitionRecordMapping

def instantiateRecord():
    record={}
    for entry in RecordFields():
        record[entry]=""
    return record

def selectValue(existingValue,newValue):
    selection=input("Two Values have tried to populate the same entry:\n1) "+existingValue+"\n2) "+newValue+"\n please select one via typing either 1 or 2 and hitting Enter.")
    if selection != "1" and selection != "2":
        print("Invalid input. Exiting.")
        exit()
    else:
        if selection=="1":
            return existingValue
        else:
            return newValue

def main():
    # start of parser boilerplate
    parser = ArgumentParser(description=" A module meant to ingest a digital acquisitions form and a staged directory and produce a record designed for use by Special Collections and the DAS.",
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
    parser.add_argument("--acquisition-record",'-a',action='append', help="Enter a noid for an accession or a " + \
                        "directory path that you need to validate against" + \
                        " a type of controlled collection"
    )
    parser.add_argument("item", help="Enter a noid for an accession or a " + \
                        "directory path that you need to validate against" + \
                        " a type of controlled collection"
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
        record=instantiateRecord()
#        print(json.dumps(instantiateRecord(),indent=4,sort_keys=True))
        for acqRecord in args.acquisition_record:
            acqDict=ReadAcquisitionRecord(acqRecord)
            for entry in AcquisitionRecordMapping():
                if entry[1] in acqDict:
                    if record[entry[0]]=="":
                        record[entry[0]]=acqDict[entry[1]]
                    else:
                        record[entry[0]]=selectValue(record[entry[0]], acqDict[entry[1]])
        print(json.dumps(record,indent=4,sort_keys=True))
#        b = Batch(args.root, args.item)
#        for item in b.find_items(from_directory=True):
#            print(item.filepath)
            
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
