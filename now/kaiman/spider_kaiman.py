from loguru import logger

from utils import request, run_func, mongo
from config import ACCESS_TOKEN, RUN_SIGN


@run_func()
def writer(row: dict or list):
    if isinstance(row, dict):
        row.update({'times': f'{RUN_SIGN}'})
    elif isinstance(row, list):
        [x.update({'times': f'{RUN_SIGN}'}) for x in row]

    mongo.insert(row, 'kaiman')


@run_func()
def auto_list():
    uri = 'https://kaiman.tradedge.cn/api/user/user_data/list'
    header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'auth-token': ACCESS_TOKEN,
        'content-type': 'application/json',
        # 'Referer': 'https://servicewechat.com/wx2fc2b286963f2cff/1/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    user_list = []

    data = {'keyword': '', 'nextKey': '', 'pageSize': '200'}
    resp = request(uri, header, data=data, json=True)

    while True:
        for user in resp.get('data').get('list'):
            user_id = user.get('userId')
            if user_id not in user_list:
                user_list.append(user_id)
                writer(user)
            else:
                logger.info(f'重复 - {user_id}')
        # writer(resp.get('data').get('list'))

        data['nextKey'] = resp.get('data').get('nextKey')
        resp = request(uri, header, data=data, json=True)


if __name__ == '__main__':
    auto_list()
