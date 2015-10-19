
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

def add_to_digitalobject(item, pattern_groups, mapping_info, objects=[]):

    assert isinstance(mapping_info, ConfigParser)
    assert isinstance(item, Item)
    assert isinstance(pattern_groups, tuple)
    group = pattern_groups
    is_it_valid = validate_filename(item.canonical_filepath)
    if is_it_valid:
        identifier_parts = mapping_info.get('Object',
                                            'identifier'). \
                                            split(',')
        identifier = []
        for l in identifier_parts:
            positions = mapping_info.get('Object', l)
            if positions.find(',') != -1:
                position = int(positions.split(',')[0])
            else:
                position = int(positions)
            identifier.append(group[position])
        potential_identifier = '-'.join(identifier)

        is_an_object_already_present = [x for x in objects \
                                        if x.get_identifier() == \
                                        potential_identifier]
        print(objects)
        if is_an_object_already_present:
            the_object = is_an_object_already_present[0]
            objects.append(the_object)
        else:
            the_object = DigitalObject(identifier)
        the_object.add_object_file(the_object)

    else:
        return False
    return objects

# def validate_filename(filepath):
#     assert isinstance(filepath, str)
#     header = re_compile('^\d{4}-\d{3}/')
#     check_for_scrc_header = header.search(filepath)
    
#     if header.search(filepath):
#         header, adjusted_filepath = re_split(header,filepath)
#         filepath_items = re_split('/|-|_',
#                                   adjusted_filepath \
#                                   [:adjusted_filepath.find('.')])
#     else:
#         filepath_items = re_splite('/|_|-',filepath)
#     for label in mapping_info.get('Object', 'labels').split(','):
#         label_positions = mapping_info.get('Object', label)
#         if label_positions.find(',') != -1:
#             label_positions = [int(x) \
#                                for x in label_positions.split(',')]
#         else:
            
#             label_positions = [int(label_positions)]
            
#         if False in [filepath_items[x] == \
#                      filepath_items[y] \
#                      for x,y in combinations(label_positions,2)]:
#             return False
#     return True

def validate_filename_id_placement(filename_parts, id_parts):
    for id_nums in id_parts:
        if id_nums.find(',') != -1:
            n_items = [int(x) for x in id_nums.split(',')]
            print(n_items)
            for t in n_items:
                print(filename_parts[t])
        else:
            print(filename_parst[int(id_nums)])
            
    # for x in id_parts:
    #     l = x.split(',')
    #     prev = None
    #     for i in l:
    #         if prev:
    #             if current == prev:
    #                 pass
    #             else:
    #                 return False
    #     return True
    #     # for n in x.split(','):
    #     #     current = filename_parts[int(n)]
    #     #     if prev == "":
    #     #         next
    #     #     elif current != prev:
    #     #         return False
    # return True
        

def validate_filename(filepath):
     test = find_pattern_in_a_string('^\d{4}-\d{3}', filepath)
     if test:
         return re_split('^\d{4}-\d{3}', filepath)[1]
     else:
         return None

def split_filepath_into_list_of_words(filepath):
    c = re_split('/|-|_', filepath)
    if c[0] == '':
        return c[1:]
    else:
        return c

def find_pattern_in_a_string(pattern, a_string):
    pattern = re_compile(pattern)
    if not pattern.search(a_string):
        return None
    return pattern
    

def get_truthiness_of_list(a_list):
    o = True
    for n in a_list:
       o = o&n
       if not o:
           break
    return 0

def find_identifier_in_list(potential_identifier, a_list):
    return [x for x in a_list if x.get_identifier() == potential_identifier]

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
            new_filepath = validate_filename(item.canonical_filepath)
            
            if new_filepath:
                
                t = split_filepath_into_list_of_words(new_filepath)[:-1]

                if search_pattern.status == True:
                    groups = search_pattern.data.groups()
                    c = validate_filename_id_placement(t,
                            [args.object_mapping.get('Object', l)
                             for l in args.object_mapping.get('Object',
                                                'identifier').split(',')])
            
                
                # did_it_add = add_to_digitalobject(item,
                #                                   search_pattern.data.groups(),
                #                                   args.object_mapping,
                #                                   objects = all_objects)

                elif page_search_pattern.status == True:
                    groups = page_search_pattern.data.groups()
                    c = validate_filename_id_placement(t,
                            [args.object_mapping.get('Object', l)
                             for l in args.object_mapping.get('Object',
                                                'identifier').split(',')])
                    logger.debug(c)
                # did_it_add = add_to_digitalobject(item,
                #                                   page_search_pattern.data. \
                #                                   groups(),
                #                                   args.page_mapping,
                #                                   objects = all_objects)


            else:
                logger.error("{path} is invalid". \
                             format(path = item.filepath))
                
            # if not did_it_add:
            #     logger.error("{path} could not be made part ".format(path = \
            #                                                 item.filepath) + \
            #             "of a digital object according to mapping provided")
        print(all_objects)
        return 0
    except KeyboardInterrupt:
        logger.error("Program aborted manually")
        return 131

if __name__ == "__main__":
    _exit(main())
