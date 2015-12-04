def verbose():
    from logging import Formatter
    from getpass import getuser

    return Formatter("[%(levelname)s] [%(asctime)s] [%(filename)s] " +
                     "[%(name)s] ["+getuser()+"] = %(message)s",
                     datefmt="%Y-%m-%dT%H:%M:%S")


def default():
    from logging import Formatter
    return Formatter("[%(levelname)8s] [%(asctime)s] = " +
                     "%(message)s",
                     datefmt="%Y-%m-%dT%H:%M:%S")


def server():
    from logging import Formatter
    return Formatter("[%(levelname)8s] [%(asctime)s] [%(reportedip)15s] " +
                     "[%(manualip)15s] [%(user)s] [%(process)d] " +
                     "[%(filename)s] [%(name)s] [%(relativeCreated)d] " +
                     "= %(message)s",
                     datefmt="%Y-%m-%dT%H:%M:%S")
