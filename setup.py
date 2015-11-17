from distutils.core import setup

setup(
    name = 'uchicagoldr',
    version = '1.0.0',
    author = "Tyler Danstrom,Brian Balsamo",
    author_email = "tdanstrom@uchicago.edu,balsamo@uchicago.edu",
    packages = ['uchicagoldr','uchicagoldrsips'],
    description = """\
    A set of base classes for interacting with University of Chicago library 
    digital repository objects
    """,
    keywords = ["uchicago","repository","file-level","processing"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = open('README.txt').read(),
    install_requires = ['python-magic == 0.4.6',
                        'SQLAlchemy >= 1.0.8'])
