import os
import json
import pymysql
from config import DOMAIN, logger
from config import DATABASES, DEBUG
from utils.soup import DealSoup
from utils.request import Query
from utils.excel_opea import ExcelOpea

req = Query().run
soup = DealSoup().judge
excel = ExcelOpea()

header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':
    'gzip, deflate, br',
    'Accept-Language':
    'zh-CN,zh;q=0.9',
    'Cookie':
    '__cfduid=dbed7513b92a9511827ce5735fb1192c71582013128; JSESSIONID=ab3c9f53-2c30-43fa-9415-b549945decb6; SERVER=WZ6myaEXBLHdYlA9/MuRSA==; MAID=2jMbtkW7Sd1iaXXY5v1L3g==; MACHINE_LAST_SEEN=2020-02-18T00%3A05%3A29.026-08%3A00; I2KBRCK=1'
}

try:
    if DEBUG:
        config = DATABASES["debug"]
    else:
        config = DATABASES["product"]

    ecnu_mysql = pymysql.connect(**config)

except pymysql.err.OperationalError as exc:
    print('登录失败！TimeoutError!')
    os._exit(0)
else:
    ecnu_cursor = ecnu_mysql.cursor()


def get_proceedings():
    with open('./proceedings.json', 'r', encoding='utf-8') as fn:
        proceedings = json.loads(fn.read())

    return proceedings.get('data').get('proceedings')


def find_title(path, pbContext=None):
    if path == 'https://dl.acm.org/doi/proceedings/10.5555/2980539':
        pbContext = soup(req(path, header=header), attr={
            'name': 'pbContext'
        }).get('content')
        with open('./01.html', 'r', encoding='utf-8') as fn:
            resp = fn.read()
    else:
        resp = req(path, header=header)
    title_list = soup(resp, attr={'class': 'issue-item__title'}, all_tag=True)
    href_list = [x.a.get('href') for x in title_list]

    if not pbContext:
        pbContext = soup(resp, attr={'name': 'pbContext'}).get('content')

    button = find_button(resp, pbContext)
    if button:
        href_list.extend(find_title(button, pbContext))

    return href_list


def find_button(content, pbContext):
    temp = soup(content, attr={'class': 'see_more'})
    if not temp:
        return
    temp = temp.find('button')
    _id = temp.get('data-id')
    doi = temp.get('data-doi')
    widgetId = soup(content, attr={
        'class': 'table-of-content-wrapper'
    }).get('data-widgetid')

    return f'{DOMAIN}/pb/widgets/lazyLoadTOCSeeMore?id={_id}&doi={doi}&widgetId={widgetId}&pbContext={pbContext}'


def get_outside(path):
    path = f'{DOMAIN}{path}'
    href_list = find_title(path)
    return href_list


def get_detail(path):
    path = f'{DOMAIN}{path}'
    resp = req(path, header=header)
    title = soup(resp, attr={'class': 'citation__title'}).get_text()

    author = [
        x.get('title') for x in soup(resp, attr={
            'ariaa-label': 'authors'
        }).findAll(attrs={'class': 'author-name'})
    ]
    author = ', '.join(author)
    publication = soup(resp, attr={'class': 'epub-section__title'}).text
    temp = soup(resp, attr={'class': 'article__body'})
    subtitle = temp.find('h2').text
    abstract = temp.find('p').text

    info = {
        '标题': title,
        '作者': author,
        '出版': publication,
        '摘要标题': subtitle,
        '摘要': abstract,
    }
    return info


def yield_proceeding():
    with open('./proceedings.json', 'r', encoding='utf-8') as fn:
        proceedings = json.loads(fn.read())

    for proceeding in proceedings.get('data').get('proceedings'):
        yield proceeding


def multi_main(proceeding):
    insert_sql = 'INSERT INTO `workoo`.`acm`(`会议`, `标题`, `作者`, `出版`, `摘要标题`, `摘要`, `proceeding`, `abs`) VALUES ("{会议}", "{标题}", "{作者}", "{出版}", "{摘要标题}", "{摘要}", "{proceeding}", "{abs}");'
    # path = proceeding.get('link')
    path = '/doi/proceedings/10.5555/2980539'
    path_list = get_outside(path)
    # path_list = ['/doi/abs/10.5555/3326943.3326944']
    for path in path_list:
        info = get_detail(path)
        info['会议'] = proceeding.get('title')
        info['proceeding'] = path
        info['abs'] = path

        for key in info:
            info[key] = pymysql.escape_string(info[key])

        sql = insert_sql.format(**info)
        try:
            ecnu_cursor.execute(sql)
        except Exception as exc:
            with open('./error.txt', 'a', encoding='utf-8') as fn:
                fn.write(f'{sql}\n')
            logger.error(exc)


def multi_query(processes=10):
    from multiprocessing import Process, Queue, Pool, freeze_support

    pool = Pool(processes)
    yield_id = yield_proceeding()

    while True:
        try:
            pool.apply_async(multi_main, (next(yield_id), ))
        except StopIteration:
            yield_id.close()
            break
        except Exception as exc:
            logger.error(exc)

    pool.close()
    pool.join()


def single_query():
    yield_id = yield_proceeding()

    # while True:
    #     try:
    #         multi_main(next(yield_id))
    #     except StopIteration:
    #         yield_id.close()
    #         break
    #     except Exception as exc:
    #         print(exc)
    while True:
        try:
            multi_main(next(yield_id))
        except StopIteration:
            yield_id.close()
            break


def main():
    excel.init_sheet(header=['会议', '标题', '作者', '出版', '摘要标题', '摘要'])
    proceedings = get_proceedings()
    for proceeding in proceedings:
        pbContext = ''
        path_list = get_outside(proceeding.get('link'))

        for path in path_list:
            info = get_detail(path)
            info['会议'] = proceeding['title']
            excel.write(info)

    excel.save()


def data_clean():
    with open('./proceedings.json', 'r', encoding='utf-8') as fn:
        proceedings = json.loads(fn.read())
    title_list = []
    excel.init_sheet(header=['会议', '标题', '作者', '摘要'])
    for proceeding in proceedings.get('data').get('proceedings'):
        title = proceeding.get('title')
        if title not in title_list:
            title_list.append(title)
        else:
            continue
        sql = 'SELECT * FROM `workoo`.`acm` WHERE `会议` = "{}" ORDER BY `abs` DESC'.format(
            pymysql.escape_string(title))
        ecnu_cursor.execute(sql)
        data = ecnu_cursor.fetchall()
        for item in data:
            # if item[6] == 'No abstract available.':
            #     print(1)
            #     continue
            excel.write([item[1], item[2], item[3], item[6]])

    excel.save()


if __name__ == "__main__":
    # main()
    # data_clean()
    # multi_query(5)
    single_query()
