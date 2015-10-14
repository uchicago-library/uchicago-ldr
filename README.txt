=================
UchicagoLdrBrowse
=================

Uchicago LDR Browse is a set of library code for programmers working on the ldr at the University of Chciago to perform a few set of common file system and ldr tasks. It is intended to be used in a command line module that the programmer builds and calls the python classes that are appropriate for the task at hand.

Batch
-----

This class provides two ways of grouping files in the ldr for processing: one groups from the ldr database, another groups from a directory. It sould be called from the find_items() method with either from_db=True or from_directory=True.

Attributes
~~~~~~~~~~

items = []
directory_path
directory_root
identifier 



Methods
~~~~~~~

find_items
walk_directory_picking_files
walk_database_query_picking_files
set_items
convert_to_relative_path
set_root_path
define_path
get_accession_from_relative_path
collect_from_directory
collect_from_database(self, database_object, queryable, query_object,
set_items
clean_out_batch

Item
----

This class provides ways of storing and manipulating and comparing files in the ldr. It should not be instantiated independently of a Batch class object.

Attributes
~~~~~~~~~~

root_path
filepath
sha256
md5
accession
mimetype
can_read
has_technical_md

Methods
~~~~~~~

test_readability
set_readability
read_file
read_file_binary
find_md5_hash
find_sha256_hash
find_hash_of_file
set_md5
set_sha256
get_md5
get_sha256
get_file_path
set_file_path
find_file_accession
set_accession
find_file_name
find_file_name_no_extension
get_accession
find_file_extension
set_file_extension
get_file_extension
find_file_size
set_file_size
get_file_size
find_file_mime_type_from_extension
find_file_mime_type_from_magic_numbers
find_file_mime_type
set_file_mime_type
get_file_mime_type
find_technical_metadata
find_a_group
get_destination_path
set_destination_path
move_into_new_location
copy_source_directory_tree_to_destination
clean_out_source_directory_tree
find_object_identifier
classify_file_type
set_destination_ownership

File System Function
--------------------

This is a collection of functions for manipulating the file system directly packaged as a convienence for programmers.

Functions
~~~~~~~~~

find_destination_path
move_into_new_location
copy_source_directory_tree_to_destination
clean_out_source_directory_tree
set_destination_ownership
