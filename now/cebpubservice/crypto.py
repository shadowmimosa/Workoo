import json
import pyDes
import base64
import binascii
from Crypto import Random
from Crypto.Cipher import DES3


class PyDes3():
    def __init__(self, key):
        """
        三重DES加密、对称加密。py2下不可用
        :param key: 密钥
        """
        # self.cryptor = pyDes.triple_des(key, padmode=pyDes.PAD_PKCS5)
        self.cryptor = pyDes.des('        ',
                                 pyDes.ECB,
                                 b"\0\0\0\0\0\0\0\0",
                                 pad=None,
                                 padmode=pyDes.PAD_PKCS5)
        if key:
            self.cryptor.setKey(key)

    def encrypt(self, text):
        """
        加密
        :param text:
        :return:
        """
        x = self.cryptor.encrypt(text.encode())
        return base64.standard_b64encode(x).decode()

    def decrypt(self, text):
        """
        解密
        :param text:
        :return:
        """
        x = base64.standard_b64decode(text.encode())
        x = self.cryptor.decrypt(x)
        return x.decode()


class DesByCrypto(object):
    def __init__(self, key):
        self.key = key
        self.iv = Random.new().read(8)  #iv值必须是8位
        self.cipher = DES3.new(key, DES3.MODE_OFB,
                               self.iv)  #密文生成器，采用MODE_OFB加密模式
        super().__init__()

    def encrypt(self, text):
        encrypt_msg = self.iv + self.cipher.encrypt('我是明文必须是八')
        return encrypt_msg

    # def decrypt(self,text):
    # #附加上iv值是为了在解密时找到在加密时用到的随机iv,加密的密文必须是八字节的整数倍，最后部分
    # #不足八字节的，需要补位
    # print '加密后的值为：', binascii.b2a_hex(encrypt_msg)  #将二进制密文转换为16进制显示

    # cipher2 = DES3.new(key, DES3.MODE_OFB, iv)  #解密时必须重新创建新的密文生成器
    # decrypt_msg = cipher2.decrypt(encrypt_msg[8:])  #后八位是真正的密文
    # print '解密后的值为：', decrypt_msg

    # Cipher = DES3.new('                ')
    # text = base64.standard_b64decode(text.encode())
    # Cipher.decrypt(text)
    # des = PyDes3(key)


if __name__ == '__main__':
    key = 'ctpstp@custominfo!@#qweASD'  # 此Key需与前端一致
    text = 'FPETfTBX/7KJh6WnLIPHw0pehnGaHd7gFf7rTx45vwmFW6lvHuMDZ3i9JmTwXwACqafVc29zifqpuzmtU51WLSu9/Ozw1xgVewV4MkwRYkWm2Uhjx5RHAd/z5i0OgZTUVVxdi8VrsA1ygJcesWSygHvQlItPSp6XRCzNLM5maeWUYJVK8zsoEuuhUrkUS1NANLqTjktwIM9KPW5dioEua+iY/zpMKsVwFxAfH8Xu44srQe4qWffyTJEvSYcI3VXLteQCaCoSmjC0ulgSxOUUstnFRHaqfQiSLTqjJZwEGYsAr/Qdn0ckCwlP5R0VYuYZjmtZI16xbN1OCl0A1rbCqy1Xfmui4UC7ryv5FLvUBb4kkIbq5Reg87U3GP1VOWaQ72w37yf5LFvTU9ZQoxbVrA70eqJnr98pTqHjwZSgEaoiq0MW0VtJ7CEDMHmlO6vSs0hH2A3d1I8/raZ2amlKgg=='
    des = PyDes3(key)
    a = des.decrypt(text)
    b = json.loads(a)
    # print(des.encrypt(text))
    print(des.decrypt(text))
{
    "NOTICE_SEND_TIME": "2020-02-18 11:49:26",
    "BULLETIN_TYPE_NAME": "招标公告",
    "NOTICE_INDUSTRIES_NAME": "其他",
    "TRADE_PLAT": "",
    "REGION_PROVINCE": "天津市",
    "REGION_NAME": "天津市 市辖区",
    "BidSectionClassifyName": "工业锅炉及辅机",
    "SERVER_PLAT": "中国招标投标公共服务平台"
}
