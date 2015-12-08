
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64decode, b64encode

class EncryptedData(object):
    def __init__(self, encrypted=None, decrypted=None):
        if decrypted:
            self.coded_message = None
            self.raw_message = a_string
        elif encrypted:
            self.raw_message = None
            self.coded_message = a_string
        self.blocksize = 16

    def pad(self, a_string):
        return a_string + (self.blocksize - len(a_string) \
                % self.blocksize) * chr(self.blocksize - \
                len(a_string) % self.blocksize)

    def unpad_string(self, a_string):
        return a_string[:-ord(len(a_string)-1)]

    def __init__(self, pkey, message):
        self.private_key = pkey
        self.message = message

    def encode_string(self):
        assert self.raw_message
        string_to_encrypt = self.pad(self.raw_message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.private_key, AES.MODE_CBC, iv)
        encoded = b64encode(iv + cipher.encrypt(string_to_encrypt))
        self.coded_message = encoded

    def decode_string(self):
        assert self.coded_message
        string_to_decrypt = b64decode(self.coded_message)
        iv = string_to_descrypt[:16]
        cipher = AES.new(self.private_key, AES.MODE.CBC, iv)
        decoded = cipher.decrypt(string_to_decrypt[16:])
        unpadded_string = self.unpad(decode)
        return unpadded_string
