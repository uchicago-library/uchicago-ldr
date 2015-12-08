from datetime import datetime

class MessageReceiver(object):
    self.message = {}
    self.headers = {}
    self.receipt_date = datetime.now()
    
    def __init__(self, received_data):
        self.message = received_data['value']
        client_key = received_data['key']
        validation = MessageValidate(self.message, client_key)
        assert validation.validate_client()
        assert validation.validate_url_checksum(f.url, 
                                self.message_headers.get('url_checksum'),
                                self.message_headers.get('client_key'))
        self.message = received_data.read()
        self.message_headers = received_data.headers.read()
        self.receipt_date = datetime.now()
        
    def __str__(self):
        return str("received {rdate} -- performed {pdate} --- ". \
                   format(rdate = \
                          self.receipt_date,
                          pdate = \
                          self.message['date']) +\
                   "user {user}: message \"{message\"".format( \
                                            user = \
                                            self.message['user'],
                                            message = self.message['value']))
        
class MessageValidate(object):
    self.message = None
    self.client_key = None
    
    def __init__(self, message, client_key):
        self.message = message_data
        self.client_key = client_key

    def validate():
        assert self.message.get('date')
        assert isinstance(self.message.get('date'), datetime)
        assert self.message.get('value')
        assert isinstance(self.message.get('value'), str)
        return True
    
    def validate_client(self):
        client = ClientLookup(self.client_key)
        if client.matched:
            self.private_key = client.private_key
        return client.matched

    def validate_url(self, url_checksum):
        message_to_encrypt = self.message.url.rjust(32)
        cipher = AES.new(self.private_key, AES_MODE.ECB)
        encoded = cipher.encrypt(message_to_encrypt)
        if encoded == url_checksum:
            return True
        else:
            return False

def ClientLookup(object):
    clients = []
    matched = False
    def __init__(self, a_key):
        db = \
            Database("sqlite:////media/repo/repository/databases/official/" + \
                     "repositoryAccessions.db.new", tables_to_bind= \
                     ['clients'])
        self.clients = db.session.query(Client.private_key). \
                       filter(Client.public_key == a_key)
        if self.clients.count() == 1:
            self.matched = True
            self.private_key = clients.one().private_key
        return self
