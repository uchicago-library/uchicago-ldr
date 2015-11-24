def DefaultTerm():
    from logging import StreamHandler

    from uchicagoldrLogging.formatters import default

    terminalHandler=StreamHandler()
    terminalHandler.setLevel('WARNING')
    terminalHandler.setFormatter(default())
    return terminalHandler

def InfoTerm():
    from logging import StreamHandler

    from uchicagoldrLogging.formatters import default

    terminalHandler=StreamHandler()
    terminalHandler.setLevel('INFO')
    terminalHandler.setFormatter(default())
    return terminalHandler

def DebugTerm():
    from logging import StreamHandler

    from uchicagoldrLogging.formatters import default

    terminalHandler=StreamHandler()
    terminalHandler.setLevel('DEBUG')
    terminalHandler.setFormatter(default())
    return terminalHandler

def DefaultFile(path):
    from logging import FileHandler

    from uchicagoldrLogging.formatters import default

    fileHandler=FileHandler(path)
    fileHandler.setLevel('WARNING')
    fileHandler.setFormatter(default())
    return fileHandler

def InfoFile(path):
    from logging import FileHandler

    from uchicagoldrLogging.formatters import default

    fileHandler=FileHandler(path)
    fileHandler.setLevel('INFO')
    fileHandler.setFormatter(default())
    return fileHandler

def DebugFile(path):
    from logging import FileHandler

    from uchicagoldrLogging.formatters import default

    fileHandler=FileHandler(path)
    fileHandler.setLevel('INFO')
    fileHandler.setFormatter(default())
    return fileHandler
