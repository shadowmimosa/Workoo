import hmac
import time
import base64
import random
import hashlib
from urllib import parse


def content_type(data):
    params = parse.quote(parse.urlencode(sorted(data.items())))

    hashing = hmac.new(
        bytes('a3a8dd89a9f833ee13a9b7e8df1d3689&', encoding='utf-8'),
        bytes(params, encoding='utf-8'), hashlib.sha1)

    return base64.b64encode(hashing.digest()).decode('utf-8')


def csrf_sign(data: dict):
    sign_str = f'{data.get("Keep-Mt")}{data.get("Keep-At")}{data.get("Keep-Csrf")}'
    sign_md5 = hashlib.md5()
    sign_md5.update(sign_str.encode('utf-8'))

    data.update({'Csrf-Sign': sign_md5.hexdigest()})

    return data


def random_header(params):
    headers = {
        'Keep-Mt': str(round(random.random() * 9999)),
        'Keep-At': str(int(time.time() / 1000)),
        'Keep-Csrf': 'cabbd66dd58ccf36c5e3119685ef39eb',
        'X-Content-Type': 'application/json;' + content_type(params),
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    return csrf_sign(headers)
