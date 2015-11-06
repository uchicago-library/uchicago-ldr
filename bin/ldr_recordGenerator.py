
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

def selectValue(field,existingValue,newValue):
    selection=input("Two Values have tried to populate the same entry: "+field+"\n1) "+existingValue+"\n2) "+newValue+"\nPlease select one via typing either 1 or 2 and hitting enter.\nSelection: ")
    if selection != "1" and selection != "2":
        print("Invalid input. Exiting.")
        exit()
    else:
        if selection=="1":
            return existingValue
        else:
            return newValue

def defaults():
    return { 'dasRecBy':'balsamo', \
             'fiscalYear':'2016', \
             'giftAckOrDeed':'False', \
             'sendInv':'False', \
             'rights':"Copyright restrictions may apply.", \
             'department':"Special Collections", \
             'permittedUseAccess':'False', \
             'permittedUseDiscover':'True', \
             'fileInfo':{}, \
             }

def populateEmpties(record):
    for entry in record:
        if isinstance(record[entry],str):
            if len(record[entry]) == 0:
                value=input("The field \""+entry+"\" is currently blank. Enter a value, or hit enter to leave it blank.\n")
                record[entry]=value
        elif isinstance(record[entry],dict):
            record[entry]=populateEmpties(record[entry])
    return record

def findEmpties(record,parentPath=""):
    empties=[]
    for entry in record:
        newPath=parentPath+"/"+entry
        if isinstance(record[entry],str) and len(record[entry]) == 0:
            empties.append(newPath)
        elif isinstance(record[entry],dict):
            empties+=findEmpties(record[entry],newPath)
    return empties

def editRecord(record,key):
    print("Editing entry \""+key+"\"")
    if isinstance(record[key],str):
        newValue=input("Please enter a new value: ")
        record[key]=newValue
    elif isinstance(record[key],dict):
        print("Key value is a dictionary. Please specify a subkey specific to that dictionary")
        print("Available subkeys:")
        for subkey in record[key]:
            print(subkey)
        childKey=input("Subkey: ")
        record[key]=editRecord(record[key],childKey)
    else:
        print("Key value is not a recognized editable data type. Sorry!")
    return record

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
    try:
        #Keep in mind that population order here matters a lot in terms of how much input the user will be asked for.

        #Instantiate a blank record with all our fields set to a blank string, for bounding loops and no funny business when we try and print it.
        record=instantiateRecord()

        #Map our defaults right into the record.
        for entry in defaults():
            record[entry]=defaults()[entry]

        #Read all the digital acquisition forms, populate the record with their info, address conflicts
        for acqRecord in args.acquisition_record:
            acqDict=ReadAcquisitionRecord(acqRecord)
            for entry in AcquisitionRecordMapping():
                if entry[1] in acqDict:
                    if record[entry[0]]=="" or record[entry[0]] == acqDict[entry[1]]:
                        record[entry[0]]=acqDict[entry[1]]
                    else:
                        record[entry[0]]=selectValue(entry[0], record[entry[0]], acqDict[entry[1]])

        #Manual input loop
        userSuppliedKey=None
        while userSuppliedKey != "":
            print(json.dumps(record,indent=4,sort_keys=True))
            print("Blank entries:")
            for entry in findEmpties(record):
                print(entry)
            userSuppliedKey=input("Enter the key of any value you would like to manually populate or change.\nEnter on a blank line to continue.\nKey: ")
            if userSuppliedKey != "":
                try:
                    editRecord(record,userSuppliedKey)
                except KeyError:
                    print("WARNING: That key doesn't appear to be in the record root.")

            

        b = Batch(args.root, args.item)
        for item in b.find_items(from_directory=True):
            itemDict={}
            uid=item.get_file_path()  #This is where the UID should go, once we settle on how we are generating them
            itemDict['fileSize']=item.find_file_size()
            itemDict['fileMime']=item.find_file_mime_type()
            itemDict['fileHash']=item.find_sha256_hash()
            record['fileInfo'][uid]=itemDict
        print(json.dumps(record,indent=4,sort_keys=True))
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
