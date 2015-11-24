def MasterLogger():
    from logging import Formatter,getLogger
    from logging.handlers import SocketHandler

    remoteAddress=None
    remotePort=None

    logger=getLogger('lib.uchicago.repository.logger')
    logger.setLevel('DEBUG')

#    networkHandler=StreamHandler(remoteAddress,remotePort)

    return logger
