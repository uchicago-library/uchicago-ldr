from distutils.core import setup

setup(
    name = "ldr",
    packages = ["ldr"],
    version = "1.0.0",
    description = "A set of base classes for interacting with University" + \
    " of Chicago library digital repository objects"
    author = ["Tyler Danstrom","Brian Balsamo],
    author_email = ["tdanstrom@uchicago.edu","balsamo@uchicago.edu"]
    keywords = ["uchicago","repository","file-level","processing"]
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
    A set of base classes for interacting with University of Chicago library 
    digital repository objects
    """
