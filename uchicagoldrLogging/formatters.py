def default():
    from logging import Formatter
    from getpass import getuser

    return Formatter("[%(levelname)s] [%(asctime)s] [%(filename)s] ["+getuser()+"] = %(message)s",datefmt="%Y-%m-%dT%H:%M:%S") 

def sparse():
    from logging import Formatter
    return Formatter("[%(levelname)s] [%(asctime)s] = %(message)s",datefmt="%Y-%m-%dT%H:%M:%S") 
