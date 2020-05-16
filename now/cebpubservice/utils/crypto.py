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


# -*- coding: utf-8 -*-

import base64
import traceback

from Crypto.Cipher import AES


class Crypto:
    def __init__(self, raw_key):
        """
        raw_key: 64位初始密钥（含逗号为65位），该密钥从KMS获取
        bs: 建议设置为16，则以128位（16字节）分组加密和解密数据
        mask: 用与对密钥进行轮异或处理
        key: aes密钥
        iv: 密钥向量
        """

        self.bs = 16
        self.mask = [
            1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1
        ]

        self.key, self.iv = self._key_init(raw_key)

    def _key_init(self, raw_key):
        """
        aes密钥及向量的初始化，需要初始密钥
        :return: （aes密钥，密钥向量）
        """
        byte_key = bytearray(raw_key, 'utf-8')
        mask_key = [i ^ j for i, j in zip(byte_key, self.mask)]

        self.key = bytearray([i for i in mask_key[33:]]).decode('utf-8')
        self.iv = bytearray([i for i in mask_key[:32]]).decode('utf-8')

        return self.key, self.iv

    def _pad(self, s):
        """
        数据预处理
        :param s: 待加密的字符串
        :return: 符合aes加密要求的输入
        """
        return s + (self.bs - len(s) % self.bs) * chr(self.bs -
                                                      len(s) % self.bs)

    def _unpad(self, s):
        """
        恢复处理
        :param s: 解密后的字符串
        :return: 原始字符串，未做任何处理之前的数据
        """
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, content):
        """
        加密
        :param content: 待加密文本
        :return: 加密后的文本
        """
        content = str(content)
        if len(content) == 0:
            return False
        try:
            content = self._pad(content)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv[:16])
            return base64.b64encode(cipher.encrypt(content))
        except:
            traceback.print_exc()
            return False

    def decrypt(self, content):
        """
        解密
        :param content: 待解密文本
        :return: 解密后的文本
        """
        # content = str(conte


if __name__ == '__main__':
    key = ''
    text = ''
    des = PyDes3(key)