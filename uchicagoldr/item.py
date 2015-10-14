from collections import namedtuple
from hashlib import md5, sha256
from magic import from_file
from os import access, chown, listdir, mkdir, rmdir, stat, R_OK, walk
from os.path import dirname, exists, join, relpath, splitext, basename
from mimetypes import guess_type, read_mime_types
from re import compile as re_compile
from shutil import move

class Item(object):
    """
    This class holds the data for each regular file in a new batch
    """
    
    root_path = ""
    filepath = ""
    sha256 = ""
    md5 = ""
    accession = ""
    mimetype = ""
    can_read = False
    has_technical_md = False
    
    def __init__(self, path, root):
        self.root_path = root
        self.filepath = join(root, path)
        self.set_readability(self.test_readability())

    def test_readability(self):
        if access(self.filepath, R_OK):
            return True
        else:
            return False

    def set_readability(self, readable_notice):
        self.can_read = readable_notice

    def read_file(self):
        with open(self.filepath,'r') as f:
            fileData=f.read()
        return fileData

    def read_file_binary(self):
        with open(self.filepath,'rb') as f:
            fileData=f.read()
        return fileData

    def find_md5_hash(self):
        return self.find_hash_of_file(md5)

    def find_sha256_hash(self):
        return self.find_hash_of_file(sha256)

    def find_hash_of_file(self, hash_type, blocksize=65536):
        def check():
            if hash_type.__name__ == sha256.__name__ or \
               hash_type.__name__ == md5.__name__:
                return True
            else:
                return False
        assert check()
        hash = hash_type()
        afile = open(self.filepath,'rb')
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hash.update(buf)
            buf = afile.read(blocksize)
        return hash.hexdigest()

    def set_md5(self, hash_value):
        self.md5 = hash_value

    def set_sha256(self, hash_value):
        self.sha256 = hash_value

    def get_md5(self):
        return self.md5

    def get_sha256(self):
        return self.sha256

    def get_file_path(self):
        return self.filepath

    def set_file_path(self,new_file_path):
        self.file_path=new_file_path

    def find_file_accession(self):
        relative_path = relpath(self.filepath, self.root_path)
        accession, *tail = relative_path.split('/')
        return accession
    
    def set_accession(self, identifier):
        if re_compile('\w{13}').match(identifier):
            self.accession = identifier
        else:
            raise ValueError("You did not pass a valid noid")

    def find_file_name(self):
        return basename(self.filepath)

    def find_file_name_no_extension(self):
        return splitext(basename(self.filepath))[0]
        
    def get_accession(self):
        return self.accession

    def find_file_extension(self):
        filename = basename(self.filepath)
        return splitext(filename)[1] 

    def set_file_extension(self, value):
        self.file_extension = value
        
    def get_file_extension(self):
        return self.file_extension

    def find_file_size(self):
        return stat(self.filepath).st_size

    def set_file_size(self, size_info):
        if isinstance(size_info, int):
            self.file_size = size_info
        else:
            raise ValueError("You did not pass an integer.")

    def get_file_size(self):
        return self.file_size

    def find_file_mime_type_from_extension(self):
        try:
            return guess_type(self.filepath)[0]
        except Exception as e:
            return (False,e)

    def find_file_mime_type_from_magic_numbers(self):
        try:
            return from_file(self.filepath, mime=True)
        except Exception as e:
            return (False,e)

    def find_file_mime_type(self):
        errors = []
        try:
            mimetype = self.find_file_mime_type_from_extension()
        except Exception as e:
            try:
                mimetype = self.find_file_mime_type_from_magic_number()
            except Exception as e:
                pass
        return mimetype

    def set_file_mime_type(self, mimetype_value):
        self.mimetype = mimetype_value

    def get_file_mime_type(self):
        return self.mimetype

    def find_technical_metadata(self):
        fits_filepath = join(self.filepath,'.fits.xml')
        if exists(fits_filepath):
            self.has_technical_md = True
        else:
            pass
        return True

    def find_a_group(self):
        print("testing...")
        return True     

    def get_destination_path(self, new_root_directory):
        path_sans_root = relpath(self.filepath, self.root_path)
        destination_full_path = join(new_root_directory, path_sans_root)
        self.destination = destination_full_path
        return True

    def set_destination_path(self, new_path):
        self.destination = new_path

    def move_into_new_location(self):
        try:
            move(self.filepath, self.destination)
            return (True,None)
        except Exception as e:
            error = e
            return (False,e)

    def copy_source_directory_tree_to_destination(self):
        destination_directories = dirname(self.destination).split('/')
        directory_tree = ""
        for f in destination_directories:
            directory_tree = join(directory_tree,f)
            if not exists(directory_tree):
                try:
                    mkdir(directory_tree,0o740)
                except Exception as e:
                    return (False,e)
        return (True,None)
    
    def clean_out_source_directory_tree(self):
        directory_tree = dirname(self.filepath)
        for src_dir, dirs, files in walk(directory_tree):
            try:
                rmdir(src_dir)
                return (True,None)
            except Exception as e:
                return (False,e)
    
    def find_object_identifier(self, control_type_data):
        object_pattern = control_type_data.get('object')
        assert object_pattern
        pattern_search = re_compile(object_pattern).search(self.filepath)
        if pattern_search:
            return namedtuple("data", "valid keys")( \
                                                     True,
                                                     pattern_search.groups() \
            )
        else:
            return namedtuple("data", "valid keys")( \
                                                     False,
                                                     None \
            )

    def classify_file_type(self, control_type_data):
        page_pattern = control_type_data.get('page_file')
        object_pattern = control_type_data.get('object_file')
        page_pattern_search = re_compile(page_pattern).search(self.filepath)
        object_pattern_search = re_compile(object_pattern). \
                                search(self.filepath)
        pagenumber = None
        if page_pattern_search:
            
            groups = page_pattern_search.groups()
            pagenumber = groups[-2]
            pagenumber = pagenumber.lstrip('0')
            tag = "page_file"
        elif object_pattern:
            tag = "object_file"
        else:
            tag = "undefinable"
        self.tag = tag
        if pagenumber:
            self.pagenumber = pagenumber

    def set_destination_ownership(self, user_name, group_name):
        uid = getpwnam(user_name).pw_uid
        gid = getgrnam(group_name).gr_gid
        try:
            chown(self.destination, uid, gid)
            return (True,None)
        except Exception as e:
            return (False,e)
