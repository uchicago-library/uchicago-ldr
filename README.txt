=================
UchicagoLdrBrowse
=================

Uchicago LDR Browse is a set of library code for programmers working on the ldr at the University of Chciago to perform a few set of common file system and ldr tasks. It is intended to be used in a command line module that the programmer builds and calls the python classes that are appropriate for the task at hand.

Batch
-----

This class provides two ways of grouping files in the ldr for processing: one groups from the ldr database, another groups from a directory. It sould be called from the find_items() method with either from_db=True or from_directory=True.

Item
----

This class provides ways of storing and manipulating and comparing files in the ldr. It should not be instantiated independently of a Batch class object.

File System Function
--------------------

This is a collection of functions for manipulating the file system directly packaged as a convienence for programmers.
