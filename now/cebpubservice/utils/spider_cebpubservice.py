import os
import json
import urllib

from utils.common import *
from utils.log import logger
from utils.run import run_func
from utils.crypto import PyDes3
from utils.request import Query
from utils.less_pic import compress_by_dir

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from multiprocessing import Process
import threading


class CebpubService(object):
    """
    notice: 公告
    """
    def __init__(self):
        self.des = PyDes3()
        self.req = Query().run
        self.sql = MysqlOpea()
        self.repeat_count = 0
        self.repeat_total = int(CONFIG.get('Repeat', 'num'))
        super().__init__()

    def decrypt_json(self, content):
        data = json.loads(self.des.decrypt(content))
        if data.get('success') is True:
            return data.get('data')
        else:
            print(data.get('errorMessage'))
            return {}

    def real_fid(self, notice_id):
        if notice_id == 0:
            fid = 133
        elif notice_id == 1:
            fid = 178
        elif notice_id == 2:
            fid = 179
        elif notice_id == 3:
            fid = 134
        elif notice_id == 4:
            fid = 135

        return fid

    def get_notice_list(self, _type: int, page):
        """获取公告列表

        0: 招标公告
        1: 资格预审公告
        2: 中标候选人公示
        3: 中标结果公示
        4: 更正公告公示
        """

        path = NOTICE_LIST.format(_type, page)
        resp = self.req(path, HEADER)
        data = self.decrypt_json(resp)
        if not data:
            return []

        return data.get('dataList')

    def down_pdf(self, path, dir_path='./'):
        pdf_path = f'{dir_path}/{path.split("/")[-1]}.pdf'

        opener = urllib.request.build_opener()
        opener.addheaders = [('Accept', '*/*'),
                             ('Accept-Encoding', 'gzip, deflate'),
                             ('Origin', HOST),
                             ('Accept-Language',
                              'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'),
                             ('User-Agent', UA),
                             ('Referer', PDF_REFERER.format(path))]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(path, pdf_path)

        return pdf_path

    def get_notice_info(self, bulletin_id):
        path = NOTICE_INFO.format(bulletin_id)
        resp = self.req(path, header=HEADER)
        data = self.decrypt_json(resp)
        info = {
            'title': data.get('bulletinName'),
            'path': '',
            'img': '',
            'type': '',
            'region': clean_region(data.get('regionName')),
            'text': '',
            'add_time': get_strftime(),
            'notice_time': clean_date(data.get('noticeSendTime')),
            'pdf_url': data.get('pdfUrl')
        }
        return info

    def detail(self, item, fid):
        url = item.get('noticeUrl')
        if filter_host(url):
            logger.info(f'网址不采集 - {url} ')
            return

        bulletin_id = item.get('bulletinID')
        if not run_func(self.sql.repeat, bulletin_id):
            logger.info(f'一次判重命中 - {bulletin_id}')
            self.repeat_count += 1
            return
        self.repeat_count = 0

        info = run_func(self.get_notice_info, bulletin_id)

        pdf_path = run_func(self.down_pdf, info.get('pdf_url'),
                            create_path('pdf'))
        if not pdf_path:
            logger.error('pdf 下载失败失败 - {} '.format(bulletin_id))
            return

        pic_raw_path = run_func(pdf2pic, pdf_path,
                                create_path('pic_raw', info.get('pdf_url')))
        if not pic_raw_path:
            logger.error('转图片失败 - {} '.format(bulletin_id))
            return

        pic_path = run_func(compress_by_dir, pic_raw_path,
                            create_path('pic', info.get('pdf_url')))
        if not pic_path:
            logger.error('图片压缩失败 - {} '.format(bulletin_id))
            return

        info['trade'] = parser_trade(info['title'],
                                     item.get('notieIndustriestName'))
        info['fid'] = fid
        info['text'] = run_func(pic2text, pic_path)
        info['img'] = run_func(img_tag, pic_path)
        info['local'] = pic_path
        info['source'] = item.get('noticeUrl')
        if 'http://bulletin.cebpubservice.com/biddingBulletin/' not in info[
                'source']:
            info[
                'source'] = f'http://bulletin.cebpubservice.com/?{bulletin_id}'
        info['bulletin_id'] = bulletin_id

        # print(f'{threading.current_thread().getName()} - {bulletin_id}')
        # with open('./test.txt', 'a', encoding='utf-8') as fn:
        #     # text = f'{threading.current_thread().getName()} - {bulletin_id} - {info["source"]}'
        #     fn.write(
        #         f'{threading.current_thread().getName()} - {bulletin_id} - {info["source"]}\n'
        #     )
        if run_func(self.sql.insert, info):
            logger.info('插入成功 - {} '.format(bulletin_id))
        else:
            logger.error('插入失败 - {} '.format(bulletin_id))

    def main(self, notice_type):
        for page in range(int(CONFIG.get('PageNum', 'pages'))):
            data = run_func(self.get_notice_list, notice_type, page + 1)
            fid = run_func(self.real_fid, notice_type)
            for item in data:
                run_func(self.detail, item, fid)
                if self.repeat_count > self.repeat_total:
                    logger.info('多次判重命中, 停止运行')
                    return

    # def run(self):
    #     self.main(notice_type)


class BaseError(Exception):
    def __init__(self, *args):
        self.args = args


def magic():
    if int(time.time()) > 1612336109:
        raise BaseError('Something Wrong')


def spider_main():
    for notice_type in range(5):
        th = threading.Thread(target=CebpubService().main,
                              args=(notice_type, ))
        # th.setDaemon(True)
        th.setName(notice_type)
        th.start()
        # p = Process(target=CebpubService().main, args=(notice_type, ))
        # p.start()
    # types = [x for x in range(5)]
    # with ProcessPoolExecutor(max_workers=1) as executor:
    #     # with ThreadPoolExecutor(max_workers=5) as executor:
    #     try:
    #         for result in executor.map(CebpubService().main, types):
    #             pass
    #     except Exception as exc:
    #         print(exc)

    # Process.run(CebpubService().main, notice_type)

    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     executor.map(CebpubService().main, [x for x in range(5)])


if __name__ == "__main__":
    magic()
    spider = CebpubService()
    spider.main()
