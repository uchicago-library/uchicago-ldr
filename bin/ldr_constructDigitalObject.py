
__author__ = "Tyler Danstrom"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "0.0.1"
__maintainer__ = "Tyler Danstrom"
__email__ = "tdanstrom@uchicago.edu"
__status__ = "Prototype"
__description__ = "This is a program for creating digital objects to " + \
                  "conform with a defined specification"


from argparse import Action, ArgumentParser
from configparser import ConfigParser
from hashlib import md5
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit
from os.path import exists
from re import compile as re_compile
from sqlalchemy import Table

from uchicagoldr.batch import Batch
from uchicagoldr.item import Item
from uchicagoldr.database import Database
from uchicagoldr.digitalobject import DigitalObject

class ReadMapping(Action):
    def __call__(self,parser,namespace,value,option_string=None):
        assert exists(value)
        config = ConfigParser()
        config.read(value)
        try:
            pattern = config.get('Object', 'pattern')
        except KeyError:
            raise ValueError("your map is missing a pattern")
        try:
            labels = config.get('Object', 'labels')
        except KeyError:
            raise ValueErorr("your map is missing a label")
        labels = labels.split(',')
        for label in labels:
            try:
                num = config.get('Object', label)
            except KeyError:
                raise ValueError("your map is missing a " + \
                        "definition for {label}".format(label = label))
        setattr(namespace,self.dest,config)

def main():
    parser = ArgumentParser(description = "{description}". \
                            format(description = __description__),
                            epilog="{copyright}; ". \
                            format(copyright = __copyright__) + \
                            "written by {author} <{email}>.". \
                            format(author = __author__,
                                   email = __email__)) 
    parser.add_argument("-v", help = "See the version of this program",
                        action = "version", version = __version__)
    parser.add_argument(  
                         '-b', '-verbose', help = "set verbose logging",
                         action = 'store_const', dest = 'log_level',
                         const = INFO \
    )
    parser.add_argument( \
                         '-d', '--debugging', help = "set debugging logging",
                         action = 'store_const', dest = 'log_level',
                         const = DEBUG \
    ) 
    parser.add_argument( \
                         '-l', '--log_loc', help = "save logging to a file",
                         action = "store_const", dest = "log_loc",
                         const = './{progname}.log'. \
                         format(progname = __file__) \
    )
    parser.add_argument( \
                         '--db_url', help = "Enter a db url",
                         action = 'store' \
    )
    parser.add_argument( \
                         '--root',help = "Enter the root of the repository",
                         action = 'store')
    parser.add_argument( \
                         '--object-mapping',help = "Enter a mapping for " + \
                         "object pattern groups", action = ReadMapping \
    )
    parser.add_argument( \
                         '--page-mapping',help="Enter a mapping for " + \
                         "page pattern groups", action = ReadMapping \
    )
    parser.add_argument( \
                         'accessions', nargs = "*", action = 'store',
                         help = "Enter 1 or more accession " + \
                         "identifiers to process" \
    )
    args = parser.parse_args()
    log_format = Formatter( \
                            "[%(levelname)s] %(asctime)s  " + \
                            "= %(message)s",
                            datefmt = "%Y-%m-%dT%H:%M:%S" \
    )
    global logger
    logger = getLogger( \
                        "lib.uchicago.repository.logger" \
    )
    ch = StreamHandler()
    ch.setFormatter(log_format)
    try:
        logger.setLevel(args.log_level)
    except TypeError:
        logger.setLevel(INFO)
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    db = Database(args.db_url, ['record','file'])
    
    class Record(db.base):
            __table__ = Table('record', db.metadata, autoload=True)
        
    class File(db.base):
            __table__ = Table('file', db.metadata, autoload=True)

    query = db.session.query(File).filter(File.accession.in_(args.accessions))
    if args.root:
        batch = Batch(args.root, query = query)
        items  = batch.find_items(from_db = True)
        batch.set_items(items)
    else:
        raise ValueError("need to include a root")
    try:
        all_objects = []
        for item in batch.get_items():
            accession = item.find_file_accession()
            item.set_accession(accession)            
            canon = item.find_canonical_filepath()            
            item.set_canonical_filepath(canon)

            search_pattern = item.find_matching_object_pattern( \
                    re_compile(args.object_mapping.get('Object', 'pattern')) \
            )
            
            page_search_pattern = item.find_matching_object_pattern( \
                    re_compile(args.page_mapping.get('Object','pattern'))
            )
        
            if search_pattern.status == True:
                logger.debug("it's an object file")
                identifier_parts = args.object_mapping.get('Object',
                                                           'identifier'). \
                                                           split(',')
                logger.debug(identifier_parts)
                group = search_pattern.data.group()
                logger.debug(group)
                potential_identifier  = '-'.join(search_pattern.data.group())
                
            elif page_search_pattern.status == True:
                logger.debug("it's a page file")
                identifier_parts = args.page_mapping.get('Object',
                                                         'identifier'). \
                                                         split(',')
                logger.debug(identifier_parts)
                group = page_search_pattern.data.groups()
                logger.debug(group)
                potential_identifier = '-'.join(page_search_pattern.data.group())
            else:
                logger.error("{path} is invalid".format(path = item.filepath))
            # if search_pattern.status == True:
                
            #     potential_identifier = '-'.join(search_pattern.data.groups())
            #     project_position = args.object_mapping. \
            #                        get('Object', 'project')
            #     is_an_object_already_present = [x for x in all_objects \
            #                                     if x.get_identifier() == \
            #                                     potential_identifier]
            #     if not is_an_object_already_present:
            #         the_object = DigitalObject(potential_identifier)
            #         all_objects.append(the_object)
            #     else:
            #         the_object = is_an_object_already_present[0]
                    
            #     validate_filename_for_object = the_object. \
            #                         validate_filename(item.canonical_filepath,
            #                                           args.object_mapping,
            #                                     search_pattern.data.groups())
            #     if not validate_filename_for_object:
            #         logger.error("{path} has mismatched ".format(path = item.filepath) + \
            #                      "values in directory and filename")

            # else:
            #     page_search_pattern = item.find_matching_object_pattern( \
            #             re_compile(args.page_mapping.get('Object',
            #                                              'pattern')) \
            #     )
                
            #     if page_search_pattern.status == True:
            #         the_object.validate_filename(item.canonical_filepath,
            #                                      page_search_pattern.groups())
                    
            #         # logger.debug("{path} is a page file". \
            #         #               format(path = item.get_canonical_filepath()))
            #     else:
            #         pass
            #         # logger.debug("{path} doesn't match any pattern". \
            #         #               format(path = item.get_canonical_filepath()))

        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
