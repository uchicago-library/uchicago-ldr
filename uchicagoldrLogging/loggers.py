def MasterLogger():
    from logging import getLogger
    from logging.handlers import SocketHandler

    remoteAddress = 'localhost'
    remotePort = '9020'

    logger = getLogger('lib.uchicago.repository.logger')
    logger.setLevel('DEBUG')

    networkHandler = SocketHandler(remoteAddress, remotePort)
    logger.addHandler(networkHandler)

    return logger
