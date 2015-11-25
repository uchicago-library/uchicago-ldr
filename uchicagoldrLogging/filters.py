import logging
from uchicagoldrLogging.lib import getUserName,getUserIP

class UserAndIPFilter(logging.Filter):
    def filter(self,record):
        record.user=getUserName()
        record.ip=getUserIP()
        return True
