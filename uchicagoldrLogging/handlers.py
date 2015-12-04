def DefaultTermHandler():
    from logging import StreamHandler

    from uchicagoldrLogging.formatters import default

    terminalHandler = StreamHandler()
    terminalHandler.setLevel('WARNING')
    terminalHandler.setFormatter(default())
    return terminalHandler


def InfoTermHandler():
    from logging import StreamHandler

    from uchicagoldrLogging.formatters import default

    terminalHandler = StreamHandler()
    terminalHandler.setLevel('INFO')
    terminalHandler.setFormatter(default())
    return terminalHandler


def DebugTermHandler():
    from logging import StreamHandler

    from uchicagoldrLogging.formatters import default

    terminalHandler = StreamHandler()
    terminalHandler.setLevel('DEBUG')
    terminalHandler.setFormatter(default())
    return terminalHandler


def DefaultTermHandlerAtLevel(level):
    from logging import StreamHandler

    from uchicagoldrLogging.formatters import default

    assert(level in ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'])

    terminalHandler = StreamHandler()
    terminalHandler.setLevel(level)
    terminalHandler.setFormatter(default())
    return terminalHandler


def DefaultFileHandler(path):
    from logging import FileHandler

    from uchicagoldrLogging.formatters import default

    fileHandler = FileHandler(path)
    fileHandler.setLevel('WARNING')
    fileHandler.setFormatter(default())
    return fileHandler


def InfoFileHandler(path):
    from logging import FileHandler

    from uchicagoldrLogging.formatters import default

    fileHandler = FileHandler(path)
    fileHandler.setLevel('INFO')
    fileHandler.setFormatter(default())
    return fileHandler


def DebugFileHandler(path):
    from logging import FileHandler

    from uchicagoldrLogging.formatters import default

    fileHandler = FileHandler(path)
    fileHandler.setLevel('DEBUG')
    fileHandler.setFormatter(default())
    return fileHandler


def DefaultFileHandlerAtLevel(path, level):
    from logging import FileHandler

    from uchicagoldrLogging.formatters import default

    assert(level in ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'])

    fileHandler = FileHandler(path)
    fileHandler.setLevel(level)
    fileHandler.setFormatter(default())
    return fileHandler
