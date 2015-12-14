def getUserName():
    from getpass import getuser
    return getuser()


def getUserIP():
    from socket import gethostbyname, gethostname
    return gethostbyname(gethostname())
