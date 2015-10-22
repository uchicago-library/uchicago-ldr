
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
from itertools import combinations
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit
from os.path import exists
from re import compile as re_compile, split as re_split
from sqlalchemy import Table

from uchicagoldr.batch import Batch
from uchicagoldr.database import Database
from uchicagoldr.digitalobject import DigitalObject
from uchicagoldr.digital_object_functions import construct_identifier, \
    does_object_exist,split_filepath_into_list_of_words, validate_filename, \
    validate_filename_id_placement
from uchicagoldr.item import Item

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
                    re_compile(args.page_mapping.get('Object', 'pattern')) \
            )
            new_filepath = validate_filename(item.canonical_filepath,
                                             '^\d{4}-\d{3}')
            if new_filepath:
                header,filepath = new_filepath
                item.set_header(new_filepath[0])
                t = split_filepath_into_list_of_words(new_filepath[1])

                id_labels = args.object_mapping.get('Object', 'identifier').split(',')
                ids = []
                for n in id_labels:
                    ids.append((t[int(args.object_mapping.get('Object', n).split(',')[0])]))
                a_id = '-'.join(ids)


                l = [x for x in all_objects if x.get_identifier() == a_id]
                if l:
                    obj = l[0]
                else:
                    new = DigitalObject(a_id)
                    all_objects.append(new)
                    obj = new
                if search_pattern.status == True:
                    groups = search_pattern.data.groups()
                    obj.add_representation(item)
                    print(obj.representations)
                elif page_search_pattern.status == True:
                    groups = page_search_pattern.data.groups()
                    page_number_position = args.page_mapping.get('Object',
                                                                 'page_number')
                    part_type_position = int(args.page_mapping.get('Object', 'file_type'))
                    page_number = int(groups[int(page_number_position[0])].lstrip('0'))
                    part_type = groups[int(part_type_position)]
                    page = obj.add_page(item, page_number, part_type)
                    
            

                # identifier_parts = [int(args.object_mapping.get('Object',
                #                                                 x)[0])
                #                     for x in args. \
                #                     object_mapping.get('Object',
                #                                     'identifier').split(',')]
                # identifier = construct_identifier(identifier_parts, t)
                # existing_object = does_object_exist(identifier, all_objects)
                # if existing_object:
                #     the_object = existing_object
                # else:
                #     the_object = DigitalObject(identifier)
                #     all_objects.append(the_object)
                # if search_pattern.status == True:

                #     c = validate_filename_id_placement(t,
                #             [args.object_mapping.get('Object', l)
                #              for l in args.object_mapping.get('Object',
                #                                 'identifier').split(',')])
                #     if c:
                #         the_object.add_object_part(item, args.object_mapping)
                #     else:
                #         logger.error("there are inconsistencies in the " + \
                #                      "naming of the file {path}". \
                #                      format(path = item.filepath))

                #     groups = page_search_pattern.data.groups()
                #     c = validate_filename_id_placement(t,
                #             [args.page_mapping.get('Object', l)
                #              for l in args.object_mapping.get('Object',
                #                                 'identifier').split(',')])
                #     if c:
                #         the_object.add_page(item, args.page_mapping)
                #     else:
                #         logger.error("there are inconsistencies in the " + \
                #                      "naming of the file {path}". \
                #                      format(path = item.filepath))
            else:
                logger.error("{path} is invalid". \
                             format(path = item.filepath))


        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
