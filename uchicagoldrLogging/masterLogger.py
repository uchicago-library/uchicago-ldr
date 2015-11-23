def masterLogger():
    from logging import FileHandler,Formatter,getLogger,SocketHandler
    from logging import StreamHandler #This is a placeholder until the logging server is built

    logFormat=Formatter("[%(levelname)s %(asctime)s = %(message)s",datefmt="%Y-%m-%dT%H:%M:%S") #We won't need this once we switch over to the socket handler, thus the hardcode.
    terminalHandler=StreamHandler() #ditto as above comment

    remoteAddress=None
    remotePort=None

    logger=getLogger('lib.uchicago.repository.logger')
    logger.setLevel('DEBUG')

#    networkHandler=StreamHandler(remoteAddress,remotePort)
    logger.addHandler(terminalHandler) #To be swapped with above once server is in place
