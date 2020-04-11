from utils.request import Query
from utils.soup import DealSoup
from utils.excel_opea import ExcelOpea
from config import logger, Cookie, Detail

from urllib.parse import quote

import json
import time
import csv


def magic_time(during=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            # print('函数开始运行的时间为：', time.strftime('%Y:%m:%d %H:%M:%S', start_time))
            result = func(*args, **kwargs)
            magic = time.time() - start_time - during
            if magic < 0:
                time.sleep(-magic)
            return result

        return wrapper

    return decorator


class Deal(object):
    def __init__(self):
        super().__init__()
        self.cookie = ''
        self.req = Query().run
        self.soup = DealSoup().judge
        self.header = {
            'Host':
            's.1688.com',
            'Connection':
            'keep-alive',
            'Upgrade-Insecure-Requests':
            '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Sec-Fetch-Dest':
            'document',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site':
            'same-origin',
            'Sec-Fetch-Mode':
            'navigate',
            'Sec-Fetch-User':
            '?1',
            'Referer':
            'https://s.1688.com/company/company_search.htm?keywords=%CA%D6%BB%FA&sortType=pop&province=%BD%AD%CB%D5%2C%D5%E3%BD%AD%2C%C9%CF%BA%A3&n=y&filt=y&pageSize=30&offset=3&beginPage=2',
            'Accept-Encoding':
            'gzip, deflate, br',
            'Accept-Language':
            'zh-CN,zh;q=0.9',
            'Cookie':
            'lid=tb4986521_2013; UM_distinctid=16efd73873a497-0345fc92e578bf-2393f61-1fa400-16efd73873bbb6; taklid=cf397e6bbdb34d979c618a05f1fec48f; ali_apache_track=c_mid=b2b-1130133263|c_lid=tb4986521_2013|c_ms=1; ali_ab=223.167.225.142.1576639999959.0; cookie2=1d408f3ecf769b69e393f13af11a1c4d; t=71451373ed29e00764600c086a5b7429; _tb_token_=e36b39b5b353e; alisw=swIs1200%3D1%7C; cna=VYrvFuCa23gCAXqPyNo34007; ali_beacon_id=218.24.120.17.1584948940881.365660.0; cookie1=BqteEusRcUH9G1uzVYrl%2BV3ggflLj7wkqGocDVvUZME%3D; cookie17=UoCKETnpLTjQuw%3D%3D; sg=33b; csg=617d32a3; unb=1130133263; uc4=nk4=0%40FY4Kqaqe7ImcaVR8Wr9utYkhxaGeu7ISuQ%3D%3D&id4=0%40UOg2td%2FhHarqJooHYqTIAlDiTMWk; __cn_logon__=true; __cn_logon_id__=tb4986521_2013; ali_apache_tracktmp=c_w_signed=Y; _nk_=tb4986521_2013; last_mid=b2b-1130133263; _csrf_token=1584953099342; __rn_alert__=false; h_keys="%u9ad8%u6863%u5973%u88c5#%u624b%u673a#%u8f66%u8f7d%u9006%u53d8%u5668#%u8f66%u8f7d%u5438%u5c18%u5668#%u951f%u65a4%u62f7%u951f%u65a4%u62f7%u951f%u65a4%u62f7%u951f%u65a4%u62f7%u951f%u65a4%u62f7#%u8f66%u8f7d%u7a7a%u6c14%u51c0%u5316%u5668#mp3#%u951f%u65a4%u62f7%u951f%u65a4%u62f7mp3#%u8f66%u8f7dmp3#%u675e%ufe41%u6d47mp3"; x5sec=7b227365617263682d776562323b32223a223466653662633933373862653563323134393736383861623564666139353938434f697134764d46454f477336502b6669494c3548526f4d4d54457a4d44457a4d7a49324d7a7378227d; _is_show_loginId_change_block_=b2b-1130133263_false; _show_force_unbind_div_=b2b-1130133263_false; _show_sys_unbind_div_=b2b-1130133263_false; _show_user_unbind_div_=b2b-1130133263_false; alicnweb=touch_tb_at%3D1584960887980%7Clastlogonid%3Dtb4986521_2013; ad_prefer="2020/03/23 19:08:40"; l=dBaf6mYlq76dkURDBOCgI4mjgd_TsIRYoukoGqdwi_5IO_Y1Fi_OoPKY1Ev6cjWfta8p4dy6R6p9-etkjmDIiyQ9SCAyaxDc.; isg=BGNjXYjNOTK52PaUoDrouwkN8qcNWPealm_hpZXAtkI51IP2HC2s6-YOyqRa8k-S'
        }

    @magic_time()
    def shop_detail(self, path, pic):
        if '/detail/' in path:
            path = path.replace('/detail', '')
        header = {
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Referer': path,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': Detail
        }
        self.header['Host'] = path.replace('https://', '').split('/')[0]

        html = self.req(path=path, header=header)

        self.info['公司名'] = self.soup(html, attr={'class': 'name-text'}).text
        self.info['联系人'] = self.soup(html, attr={
            'class': 'contact-info'
        }).text.split('：')[-1]
        temp = self.soup(html, attr={'name': 'hiddenMobileNo'})

        self.info['手机'] = temp.get('value') if temp else None
        self.info['公司介绍'] = self.soup(html, attr={'class': 'detail-info'}).text
        info_data = self.soup(html, attr={'class': 'info-data'})
        self.info['公司类型'] = self.soup(info_data, 'td', all_tag=True)[3].text
        self.info['详细地址'] = self.soup(html,
                                      attr={'class': 'tb-value-data'},
                                      all_tag=True)[-1].text
        self.info['地市'] = self.info['详细地址'].split('市')[0]
        self.info['图片'] = pic
        self.info['网址'] = path.split('page/')[0]

    def main(self):
        category = ['女装 时尚都市']
        with open('./data/already.txt', 'r', encoding='utf-8') as fn:
            already = fn.read().split('\n')
        error_count = 0
        for keyword in category:
            count, page = (0, 1) if keyword != '女装 时尚都市' else (100, 3)
            keyword = quote(str(keyword).encode('gbk'))
            while count < 1000:
                self.header['Host'] = 's.1688.com'
                header = {
                    'Host': 's.1688.com',
                    'Cache-Control': 'max-age=0',
                    'Origin': 'https://s.1688.com',
                    'Upgrade-Insecure-Requests': '1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
                    'Sec-Fetch-User': '?1',
                    'Accept':
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'navigate',
                    'Referer':
                    'https://s.1688.com/company/company_search.htm?keywords=%B8%DF%B5%B5%C5%AE%D7%B0&sortType=pop&province=%BD%AD%CB%D5%2C%D5%E3%BD%AD%2C%C9%CF%BA%A3&n=y&filt=y',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cookie': Cookie
                }
                if page == 1:
                    self.header['Referer'] = 'https://auto.1688.com/'
                    path = 'https://s.1688.com/company/company_search.htm?keywords={}&sortType=pop&province=%BD%AD%CB%D5%2C%D5%E3%BD%AD%2C%C9%CF%BA%A3&&n=y&filt=y'.format(
                        keyword)
                    resp = self.req(path, header=header)
                else:
                    path = 'https://s.1688.com/company/company_search.htm?keywords={}&sortType=pop&province=%BD%AD%CB%D5%2C%D5%E3%BD%AD%2C%C9%CF%BA%A3&&n=y&filt=y&pageSize=30&offset=3&beginPage={}'.format(
                        keyword, page)

                    resp = self.req(path, header=header, data=True)

                if '亲，小二正忙，滑动一下马上回来' in resp:
                    logger.error('Change Cookie')
                    return
                time.sleep(1)
                shops = self.soup(resp,
                                  attr={'class': 'company-list-item'},
                                  all_tag=True)

                for shop in shops:
                    self.info = {}
                    title = self.soup(shop, {
                        'class': 'list-item-title-text'
                    }).text
                    title = remove_charater(title)
                    if title in already:
                        continue
                    else:
                        already.append(title)

                    link = self.soup(shop,
                                     {'offer-stat': 'morecompany'})['href']
                    # pic = shop.img.get('src')
                    # if pic is None:
                    #     pic = shop.img.get('data-lazyload-src')
                    # self.shop_detail(link, pic)
                    try:
                        pic = shop.img.get('src')
                        if pic is None:
                            pic = shop.img.get('data-lazyload-src')
                        self.shop_detail(link, pic)
                    except Exception as exc:
                        logger.error(f'detail is error - {exc}')
                    else:

                        # excel.write(remove_charater(self.info))
                        count += 1
                        write(remove_charater(self.info))

                        magic_time()

                page += 1

        excel.save()


def remove_charater(content: str):
    if isinstance(content, str):
        return content.replace('\n',
                               '').replace('\t',
                                           '').replace('\r',
                                                       '').replace(' ', '')
    elif isinstance(content, dict):
        need = {key: remove_charater(content[key]) for key in content}
        return need


def write(content=None):
    title_list = ['公司名', '联系人', '手机', '公司介绍', '公司类型', '地市', '详细地址', '图片', '网址']

    if content is None:
        need = title_list
    elif len(content) == 0:
        return
    else:
        need = [content[key] for key in title_list]

    need = [remove_charater(value) for value in need]

    with open('./data/data.csv', 'a', encoding='utf-8') as fn:
        writer = csv.writer(fn)
        writer.writerow(need)

    with open('./data/already.txt', 'a', encoding='utf-8') as fn:
        fn.write(need[0])
        fn.write('\n')


if __name__ == "__main__":
    excel = ExcelOpea()
    excel.init_sheet(
        header=['公司名', '联系人', '手机', '公司介绍', '公司类型', '地市', '详细地址', '图片', '网址'])
    Deal().main()