def defaultTerm():
    from logging import StreamHandler

    from uchicagoldrLogger.formatters import default

    formatter=default()
    terminalHandler=StreamHandler()
    terminalHandler.setLevel('WARNING')
    return terminalHandler

def infoTerm():
    from logging import StreamHandler

    from uchicagoldrLogger.formatters import default

    formatter=default()
    terminalHandler=StreamHandler()
    terminalHandler.setLevel('INFO')
    return terminalHandler

def debugTerm():
    from logging import StreamHandler

    from uchicagoldrLogger.formatters import default

    formatter=default()
    terminalHandler=StreamHandler()
    terminalHandler.setLevel('DEBUG')
    return terminalHandler

def defaultFile(path):
    from logging import FileHandler

    from uchicagoldrLogger.formatters import default

    formatter=default()
    fileHandler=FileHandler(path)
    fileHandler.setLevel('WARNING')
    return fileHandler

def infoFile(path):
    from logging import FileHandler

    from uchicagoldrLogger.formatters import default

    formatter=default()
    fileHandler=FileHandler(path)
    fileHandler.setLevel('INFO')
    return fileHandler

def debugFile(path):
    from logging import FileHandler

    from uchicagoldrLogger.formatters import default

    formatter=default()
    fileHandler=FileHandler(path)
    fileHandler.setLevel('INFO')
    return fileHandler
