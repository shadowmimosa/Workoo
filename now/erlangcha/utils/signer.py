import time
import hashlib

from utils import request
from config import APP, AUTH, FIXED, SALT


def encrypt(app=APP, timestamp=int(time.time() * 1000), fixed=FIXED):
    text = f'?auth={AUTH}&app={app}&timestamp={timestamp}&fixed={fixed}'
    md5 = hashlib.md5(SALT)
    md5.update(text.encode('utf-8'))
    secret = md5.hexdigest().lower()

    return f'{text.replace("auth=shadowmimosa&","")}&token={secret}'


class MagicError(Exception):
    def __init__(self, *args):
        self.args = args


def magic():
    path = f'http://auth.bigbe.cn/workoo/auth{encrypt()}'
    result = request(path, json=True, redirect=True)
    if result.get('code') != 200:
        raise MagicError('Something Wrong')
