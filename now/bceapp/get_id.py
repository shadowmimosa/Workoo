import json
from utils.mongo import Mongo
from utils.soup import DealSoup

soup = DealSoup().judge

with open('./raw/erp_dz.php.json', 'r', encoding='utf-8') as fn:
    data = json.loads(fn.read())

trs = soup(data.get('patient_msg'), 'tr', all_tag=True)

for tr in trs:
    info = {}
    tds = soup(tr, 'td', all_tag=True)
    info['ID'] = tr.get('id')
    info['姓名'] = tds[1].text
    info['手机号'] = tds[2].text
    info['性别'] = tds[3].text
    info['出生年月'] = tds[4].text
    info['祛痘主任'] = tds[5].text
    info['祛痘师'] = tds[6].text
    info['类型'] = tds[7].text
    info['会员等级'] = tds[8].text
    info['最后到店时间'] = tds[9].text
    info['status'] = 0

    result = Mongo.repeat(info, 'bceapp_info')
    print(f'已添加 - {result}')
