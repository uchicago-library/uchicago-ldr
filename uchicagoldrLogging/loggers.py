def MasterLogger():
    from logging import Formatter,getLogger
    from logging.handlers import SocketHandler

    from uchicagoldrLogging.formatters import verbose 

    remoteAddress='localhost'
    remotePort='9020'

    logger=getLogger('lib.uchicago.repository.logger')
    logger.setLevel('DEBUG')

    networkHandler=SocketHandler(remoteAddress,remotePort)
    logger.addHandler(networkHandler)
    
    return logger
