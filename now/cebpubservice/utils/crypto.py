import json
import pyDes
import base64
import binascii
from Crypto import Random
from Crypto.Cipher import DES3


class PyDes3():
    def __init__(self, key='ctpstp@custominfo!@#qweASD'):
        self.cryptor = pyDes.des('        ',
                                 pyDes.ECB,
                                 b"\0\0\0\0\0\0\0\0",
                                 pad=None,
                                 padmode=pyDes.PAD_PKCS5)
        if key:
            self.cryptor.setKey(key)
        super().__init__()

    def encrypt(self, text):
        x = self.cryptor.encrypt(text.encode())
        return base64.standard_b64encode(x).decode()

    def decrypt(self, text):
        x = base64.standard_b64decode(text.encode())
        x = self.cryptor.decrypt(x)
        return x.decode()


if __name__ == '__main__':
    key = ''
    text = ''
    des = PyDes3(key)