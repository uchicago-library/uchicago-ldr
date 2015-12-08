
from datetime import datetime
from urllib import urlencode
from urllib2 import Request, urlopen

class LogMessage(object):
    value = None
    client = None
    user = None
    tryDate = None
    date = None
    warnings = []

    def __init__(self, a_message, client_name, userid):
        self.value = a_message
        self.client = client_name
        self.user = userid
        self.date = datetime.now()
        self.warnings = []
        self.send_message(self)

    def send_message(self):
        m = MessageForwarder(self)

    def add_warning(self, warning):
        assert isinstance(warning, str)
        self.warnings.append(warning)

    def flag_as_unsuccessfully_sent():
        self.tryDate = datetime.now()

class MessageForwarder(object):
    message = None
    server_endpoint = "http://example.com/"
    log_key = "some_key"

    def __init__(self):
        self.message = a_message
        v, new_message = MessageValidator(self.message)
        if not isinstance(self.message.value, str):
            self.message.add_warning("not_string")
        self.forward_message_along(self.message)

    def _object_to_dict(self, message_object):
        retur vars(message_object)

    def forward_message_along(self):
        """
        This function will create a restful connection to the server endpoint and post
        the message data to the server. If the connection is successful, it will receive a 200
        and all is forgotten

        If connection is unsuccessful, pass message to the local logqueue for retrying later
        """
        dictionary = _object_to_dict(self.message)
        headers = {'client-key':'a_key',
                   'url_checksum':'a_checksum'}
        data = urlencode(dicitonary)
        request = urlencode(self.server_endpoint, data, headers)
        response = urlopen(request)
        if response.getcode() == 200:
            return True
        else:
            return False
                        
class LocalQueue(object):
    messages = []
    
    def __init__(self):
        self.messages = []

    def add_to_queue(self, message):
        assert isinstance(message, LogMessage)
        self.messages.append(message)

    def retry_sending_message(self):
        n = self.messages[0]
        forwarder = MessageForwarder(n)
        if forwarder:
            self.messages = self.messages[1:]
        
