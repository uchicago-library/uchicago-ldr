
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
from uchicagoldr.forms.recordFields import RecordFields
from uchicagoldr.forms.recordFieldsBooleans import RecordFieldsBooleans
from uchicagoldr.forms.recordFieldsValidation import RecordFieldsValidation
from uchicagoldr.forms.recordFieldsDefaults import RecordFieldsDefaults
from uchicagoldr.forms.ldrFields import LDRFields
from uchicagoldr.forms.digitalAcquisitionRead import ReadAcquisitionRecord
from uchicagoldr.forms.digitalAcquisitionMap import AcquisitionRecordMapping

def writeNoClobber(record,filepath):
    path,filename=split(filepath)
    try:
        assert(isdir(path))
        assert(len(filename)>0)
    except AssertionError:
        return False

    while exists(filepath):
        if filepath[-1].isdigit():
            nextNum=int(filepath[-1])+1
            filepath=filepath[0:-1]+str(nextNum)
        else:
            filepath=filepath+".1"

    with open(filepath,'w') as f:
        json.dump(record,f,indent=4,sort_keys=True)
    return True

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

def manualInput(record):
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

def stringToBool(string):
    string=string.lower()
    negatives=['f','false','no','n','n/a','']
    positives=['t','true','yes','y']
    for term in negatives:
        if string == term:
            return "False"
    for term in positives:
        if string == term:
            return "True"
    return string

def validate(record,validator):
    for entry in validator:
        #Eventually this is where validation of nested values should go, if required
        if type(record[entry[0]]) != str:
            continue
        for regex in entry[1]:
            while not match(regex,record[entry[0]]):
                print(entry[0]+" ("+record[entry[0]]+") does not match against a validation regex! ("+regex+")\nPlease input a new value that conforms to the required validation expression.")
                editRecord(record,entry[0])
    return record

def booleanLoop(record,bools):
    for entry in bools:
        suggestion=stringToBool(record[entry])
        if suggestion != record[entry]:
            record[entry]=selectValue(entry,record[entry],suggestion)
    return record

def createSubRecord(record,fields):
    subRecord={}
    for field in fields:
        subRecord[field]=record[field]
    return subRecord

def meldRecord(record,target,reader,mapper):
    newDict=reader(target)
    for entry in mapper():
        if entry[1] in newDict:
            if record[entry[0]]=="" or record[entry[0]] == newDict[entry[1]]:
                record[entry[0]]=newDict[entry[1]]
            else:
                record[entry[0]]=selectValue(entry[0],record[entry[0]],newDict[entry[1]])

def dummyReader(target):
    return target

def dummyMapper():
    dummyMap=[]
    for entry in RecordFields():
        dummyMap.append((entry,entry))
    return dummyMap

def generateFileEntries(root,item):
    fileInfoDict={}
    b = Batch(root, item)
    totalDigitalSize=0
    for item in b.find_items(from_directory=True):
        itemDict={}
        item.set_accession(item.find_file_accession())
        uid=sha256(join(item.get_accession(),item.find_canonical_filepath()).encode('utf-8')).hexdigest()
        itemDict['fileSize']=item.find_file_size()
        totalDigitalSize+=itemDict['fileSize']
        itemDict['fileMime']=item.find_file_mime_type()
        itemDict['fileHash']=item.find_sha256_hash()
            
        if ".presform" in item.find_file_name():
            presStable="True"
        else:
            presStable="False"

        itemDict['fileStable']=presStable

        fileInfoDict[uid]=itemDict
    return fileInfoDict

def computeTotalFileSizeFromRecord(record):
    totalSize=0
    for entry in record['fileInfo']:
        totalSize+=record['fileInfo'][entry]['fileSize']
    return totalSize

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
        meldRecord(record,RecordFieldsDefaults(),dummyReader,dummyMapper)

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
