
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
from os import _exit,listdir
from os.path import isdir,join,abspath,expandvars,split,exists
import json
from re import match
from hashlib import sha256

from uchicagoldr.batch import Batch
from uchicagoldr.item import Item

from uchicagoldrRecords.record.recordFields import RecordFields
from uchicagoldrRecords.record.recordFieldsBooleans import RecordFieldsBooleans
from uchicagoldrRecords.record.recordFieldsValidation import RecordFieldsValidation
from uchicagoldrRecords.record.recordFieldsDefaults import RecordFieldsDefaults
from uchicagoldrRecords.fields.ldrFields import LDRFields
from uchicagoldrRecords.readers.digitalAcquisitionRead import ReadAcquisitionRecord
from uchicagoldrRecords.readers.dummyReader import DummyReader
from uchicagoldrRecords.mappers.digitalAcquisitionMap import AcquisitionRecordMapping
from uchicagoldrRecords.mappers.dummyMapper import DummyMapper
from uchicagoldrRecords.record.recordWriting import instantiateRecord,meldRecord,manualInput,booleanLoop,validate,generateFileEntries,computeTotalFileSizeFromRecord,writeNoClobber,createSubRecord

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
    parser.add_argument("--out-file",'-o',help="The location where the full record should be written to disk.",required=True,action="append")
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
    try:
        print("BEGINNING")
        #Keep in mind that population order here matters a lot in terms of how much input the user will be asked for.

        #Instantiate a blank record with all our fields set to a blank string, for bounding loops and no funny business when we try and print it.
        print("Instantiating Record")
        record=instantiateRecord()

        #Map our defaults right into the record.
        print("Mapping defaults")
        meldRecord(record,RecordFieldsDefaults(),DummyReader,DummyMapper)

        #Read all the digital acquisition forms, populate the record with their info, address conflicts
        print("Reading and mapping digital acquisition records.")
        for acqRecord in args.acquisition_record:
            meldRecord(record,acqRecord,ReadAcquisitionRecord,AcquisitionRecordMapping)

        #Manual input loop
        print("Beginning Manual Input Loop")
        manualInput(record)

        #Run some automated processing over the record to clean up certain values if required.
        print("Beginning attempts at automated boolean interpretation")
        record=booleanLoop(record,RecordFieldsBooleans())
        #Validate the record fields against their stored regexes
        print("Validating...")
        record=validate(record,RecordFieldsValidation())

        #File level information population
        print("Generating file info...")
        record['fileInfo']=generateFileEntries(args.root,args.item)

        print("Computing total size")
        record['totalDigitalSize']=computeTotalFileSizeFromRecord(record)
        
        #Write two records, one which contains the entirety of the record, including potential internal information, to an internal source, and another which contains information pertinent to the LDR into the admin directory
        print("Writing whole record to out files.")
        for filepath in args.out_file:
            assert(writeNoClobber(record,filepath))

        print("Creating subrecord")
        pubRecord=createSubRecord(record,LDRFields())

        print("Attempting to write LDR subrecord into staging structure.")
        ldrRecordPath=None
        try:
            #Lets see if we are in a real (and properly formed) staging structure
            assert(len(listdir(args.item))==1)
            assert(isdir(join(args.item,listdir(args.item)[0])))
            EADPath=join(args.item,listdir(args.item)[0])
            assert(len(listdir(EADPath))==1)
            assert(isdir(join(EADPath,listdir(EADPath)[0])))
            accNoPath=join(EADPath,listdir(EADPath)[0])
            assert(len(listdir(accNoPath))==2)
            assert("data" in listdir(accNoPath) and "admin" in listdir(accNoPath))
            ldrRecordPath=join(accNoPath,"admin")+'/record.json'
        except AssertionError:
            print("You don't seem to have pointed the script at a fully qualified staging structure. Please manually specify a location to save the LDR record to, otherwise leave this line blank to save only the full record.")
            while ldrRecordPath == None:
                ldrRecordPath=input("LDR Record Path: ")
                if ldrRecordPath == "":
                    break
                if len(ldrRecordPath) > 0:
                    ldrRecordPath=abspath(expandvars(ldrRecordPath))
                    print("Attempted abspath "+ ldrRecordPath)
                if not isdir(ldrRecordPath):
                    ldrRecordPath=None

        if ldrRecordPath != "":
            writeNoClobber(pubRecord,ldrRecordPath)
            print("LDR Record written")
        else:
            print("LDR Record generation skipped.")

        print(json.dumps(record,indent=4,sort_keys=True))

        print("COMPLETE")

        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
