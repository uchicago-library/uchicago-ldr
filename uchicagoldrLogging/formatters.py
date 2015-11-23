def default():
    from logging import Formatter
    return Formatter("[%(levelname)s %(asctime)s = %(message)s",datefmt="%Y-%m-%dT%H:%M:%S") 
