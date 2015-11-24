def MasterLogger():
    from logging import Formatter,getLogger
    from logging.handlers import SocketHandler

    remoteAddress='localhost'
    remotePort='notarealport'

    logger=getLogger('lib.uchicago.repository.logger')
    logger.setLevel('DEBUG')

    networkHandler=SocketHandler(remoteAddress,remotePort)
    logger.addHandler(networkHandler)

    return logger
