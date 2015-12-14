import logging
from uchicagoldrLogging.lib import getUserName, getUserIP


class UserAndIPFilter(logging.Filter):
    def filter(self, record):
        record.user = getUserName()
        record.reportedip = getUserIP()
        return True


class ManualIPFilter(logging.Filter):
    def filter(self, record, ip):
        record.manualip = ip
        return True
