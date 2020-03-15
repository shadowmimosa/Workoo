# -*- coding:utf-8 -*-
"""
西瓜视频
获取视频真实URL
"""

import re
import requests
import random
from zlib import crc32
from base64 import b64decode


def get_video_url_api(video_id):
    """获取视频地址所在包的url"""
    r = str(random.random())[2:]
    url_part = "/video/urls/v/1/toutiao/mp4/{}?r={}".format(video_id, r)
    s = crc32(url_part.encode())
    url = "https://ib.365yg.com{}&s={}".format(url_part, s)
    return url


def get_video_url(url):
    """获取视频地址"""
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }
    resp = requests.get(url, headers=headers)
    j_resp = resp.json()
    video_url = j_resp['data']['video_list']['video_1']['main_url']
    video_url = b64decode(video_url.encode()).decode()
    return video_url


def get_video_id(url):
    """获取视频id"""
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }
    resp = requests.get(url, headers=headers)
    # 获取video_id
    return re.search("videoId: '([^\']+)'", resp.text).group(1)


def main():
    # url = 'https://www.ixigua.com/a6695286370652389896/'
    url = 'https://www.ixigua.com/a6610679501925911815/'
    #
    video_id = get_video_id(url)
    #
    video_url_api = get_video_url_api(video_id)
    #
    video_url = get_video_url(video_url_api)
    print(video_url)


if __name__ == '__main__':
    import base64
    main_url='aHR0cDovL3YzLXR0Lml4aWd1YS5jb20vZWU3ZmMzNWNlYTQ0YjY4ZWVlYWNjNWZjNjZjZGU2NmYvNWU0YTE4NWUvdmlkZW8vdG9zL2NuL3Rvcy1jbi12ZS00LzRiNjI5OTg1OTllODQ2ZDM4NTk1OWNjNmZlMTJjYTY0Lz9hPTE3NjgmYnI9NzU5JmJ0PTI1MyZjcj0wJmNzPTAmZHI9MCZkcz0xJmVyPSZsPTIwMjAwMjE3MTEyNTAxMDEwMDE0MDQ0MDgwMjU2MTlEQ0QmbHI9JnFzPTAmcmM9YW5OdmRXWjBiSGh3Y1RNelBEY3pNMEFwTm1ob096ZzRaR1ZvTjJjME5HY3paMmN4TkhNMWNXZHpObVZmTFMwMkxTOXpjMkl0WUMxZkxXRmdMVEJqWGpJMVl6WTZZdyUzRCUzRCZ2bD0mdnI9'
    a = base64.standard_b64decode(main_url)
    print(a)
    main()


# http://v6-tt.ixigua.com/5284077927635273970d59b8e6afc1e5/5e4a16eb/video/tos/cn/tos-cn-v-0000/b72e9164eca34937b98a2861f19c40b2/?a=1768&br=21014&bt=10507&cr=0&cs=0&dr=0&ds=4&er=&l=20200217113013010010054221221B55F9&lr=&qs=13&rc=M2Q2aW14bWw5bDMzZDczM0ApbmdoaGo4eHN2ZTMzZTM1eWdoYWJiZDJybXBfLS1fLS9zcy1eMGNncmdmM2YtLV4xLS06Yw%3D%3D&vl=&vr=
# http://v1-tt.ixigua.com/5bbf0c2e2363bd60c5ffc2a62c1fb499/5e4a15bc/video/tos/hxsy/tos-hxsy-ve-0004/a541532f0d5741bab41c87c45f47a7c4/?a=1768&br=11721&bt=3907&cr=0&cs=0&dr=0&ds=4&er=&l=202002171125100100140182170E2D7447&lr=&qs=0&rc=M2Q2aW14bWw5bDMzZDczM0ApPGRkZ2lnZzw8N2lpNjU6NmdoYWJiZDJybXBfLS1fLS9zc19iMTMyM182YWI0YmBfYmA6Yw%3D%3D&vl=&vr=