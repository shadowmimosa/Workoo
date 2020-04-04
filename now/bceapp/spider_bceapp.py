import os
import json

from utils.mongo import Mongo
from utils.soup import DealSoup
from utils.request import Query
from utils.excel_opea import ExcelOpea

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

req = Query().run
soup = DealSoup().judge
header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Origin': 'http://starserp.bceapp.com',
    'Referer': 'http://starserp.bceapp.com/erp/admin/qt.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'pin_code=14; PHPSESSID=1d150025ca283815ebdbca15510d315f'
}
domain = 'http://starserp.bceapp.com/erp/interface/erp_dz.php'
param = 'action=get_patient_detail_msg&patient_id={}'


def detail(ID, _id):
    data = param.format(ID)
    resp = req(domain, header=header, data=data)

    data = json.loads(resp)

    result = Mongo.repeat(data, 'bceapp_detail')
    if data.get('status') == 1:
        print(f'已完成 - {result}')
        Mongo.update({'_id': _id}, {'status': 1}, 'bceapp_info')
    else:
        print(f'状态异常 - {data.get("status")}')


def down_info():
    results = Mongo.select('bceapp_info', {'status': 0}, limit=20, _id=False)

    while results:
        for result in results:
            detail(result.get('ID'), result.get('_id'))

        results = Mongo.select('bceapp_info', {'status': 0},
                               limit=20,
                               _id=False)


def down_img(src):
    if '.' not in src:
        src = f'{src[:-4]}.jpeg'

    path = './img' + src.replace('http://xingchen-erp.bj.bcebos.com',
                                 '').replace(
                                     'http://xingchenerp.bj.bcebos.com', '')
    if os.path.isfile(path):
        return path

    resp = req(src, sign=True)

    dirpath = path.replace(path.split('/')[-1], '')
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    with open(path, 'wb') as fn:
        fn.write(resp)

    return path


def record_data(html):
    divs = soup(html, {'class': 'fix_div'}, all_tag=True)
    need = '\n'.join([div.text for div in divs])
    img = soup(html, 'img')
    if not img:
        return need, ''
    src = img.get('src')
    path = down_img(src)

    return need, f'=HYPERLINK("{path}","图片")'
    # return need, src


def mutl_record_data(result):
    # print(result)
    m_record_data = result.get("m_record_data").replace(
        'fix pt10 pl20', 'fix_div')
    records = soup(m_record_data, {'class': 'fix'}, all_tag=True)
    for record in records:
        record_data(record)


def mutl_main(results):
    # thead_pool = ThreadPoolExecutor(10)
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(mutl_record_data, results)

    # for result in results:
    #     thead_pool.submit(mutl_record_data, result)


def mutl_img():
    results = Mongo.select('bceapp_detail', limit=100, _id=False)

    while results:
        mutl_main(results)

        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     executor.map(mutl_record_data, results)
        # try:
        #     for result in executor.map(mutl_record_data, results):
        #         pass
        # except Exception as exc:
        #     print(exc)

        results = Mongo.select('bceapp_detail',
                               {'_id': {
                                   '$gt': results[-1].get('_id')
                               }},
                               limit=20,
                               _id=False)


def to_excel():
    count = 0
    results = Mongo.select('bceapp_detail', limit=20, _id=False)
    excel = ExcelOpea()
    excel.init_sheet(header=['顾客信息', '祛痘次数', '消费金额', '祛痘项目', '祛痘史', '备　　注'])
    # excel.header = ['顾客信息', '祛痘次数', '消费金额', '祛痘项目', '祛痘史', '备　　注']

    while results:
        for result in results:
            info = {}
            info[
                '顾客信息'] = f'{result.get("display_data").get("name")}{result.get("display_data").get("patient_info")}'
            info['祛痘次数'] = f'{result.get("display_data").get("treat_info")}'
            info['消费金额'] = f'{result.get("display_data").get("pay_info")}'
            info['祛痘项目'] = f'{result.get("display_data").get("disease_name")}'
            info['祛痘史'] = f'{result.get("display_data").get("qd_history")}'
            info['备　　注'] = f'{result.get("display_data").get("remark")}'
            m_record_data = result.get("m_record_data").replace(
                'fix pt10 pl20', 'fix_div')
            records = soup(m_record_data, {'class': 'fix'}, all_tag=True)

            for index, value in enumerate(records):
                title_0 = f'治疗详情-{index + 1}'
                title_1 = f'图片-{index + 1}'

                for title in [title_0, title_1]:
                    if title not in excel.header:
                        excel.header.append(title)
                try:
                    info[title_0], info[title_1] = record_data(value)
                except Exception as exc:
                    print(exc)
                    continue

            excel.write(info)
            count += 1
            print(f'已插入 - {result.get("_id")} - {count}')

        results = Mongo.select('bceapp_detail',
                               {'_id': {
                                   '$gt': result.get('_id')
                               }},
                               limit=20,
                               _id=False)

    excel.save()


def main():
    # down_info()
    to_excel()
    # mutl_img()


if __name__ == "__main__":
    main()
