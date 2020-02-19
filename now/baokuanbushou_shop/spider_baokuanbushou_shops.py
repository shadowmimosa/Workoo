import re
import json
import time
import js2py
import datetime
from bson import ObjectId

from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup
from config import DEBUG, logger, mongo, get_cookie


def magic_time():
    second = mongo['cookie'].find_one(
        {'_id': ObjectId('5e16d4b7c0000000850049b4')})['waiting']
    time.sleep(second)


def shops():
    for page in range(5000):
        header['Cookie'] = get_cookie()
        path = f'https://bkbs.baokuanbushou.com/s.stp?action=dy_shop_search&key=&cat=&sort=8&size=10&page={page}&stcallback=_jsonph32oae3dtmk'
        resp = req(path, header=header)
        if resp:
            json_obj = run_func(re.search, json_pattern, resp)
            if json_obj:
                data = json.loads(json_obj.group(1))
            else:
                data = None
        if data:
            need_insert = []
            for item in data['items']:
                info = {}
                info['company_name'] = item['company_name']
                info['spider_type'] = 'shops'
                info['Original information'] = item
                need_insert.append(info)

            if need_insert:
                run_func(mongo["baokuanbushou"].insert_many, need_insert)
            else:
                logger.info('shops down')
                break
        else:
            logger.error('no data')


def main():
    shops()


req = Query().run
json_pattern = re.compile(r'^_json.*\(([\s\S]*)\)$')

header = {
    'Host': 'bkbs.baokuanbushou.com',
    'Accept': '*/*',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'no-cors',
    'Referer': 'https://bkbs.baokuanbushou.com/s.stp?action=dyhome_pc',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

if __name__ == "__main__":
    main()