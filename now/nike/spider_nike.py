import re
import json
import time
import random
from multiprocessing import Pool, Lock, freeze_support
from multiprocessing.managers import BaseManager

from utils.run import run_func
from utils.request import Query
from utils.excel_opea import ExcelOpea
from config import logger


def judge_sku(itme: dict):
    skus = [x['localizedSize'] for x in itme['skus']]
    skuid = [x['skuId'] for x in itme['skus']]
    available = [x['skuId'] for x in itme['availableSkus']]

    info = []

    for sku in skuid:
        if sku in available:
            info.append('有货')
        else:
            info.append('无货')

    return skus, info


def get_detail(path, excel=None, lock=None):
    global INFO

    if '{countryLang}' in path:
        path = path.replace('{countryLang}', country_lang)
        path = f'{host}/{path}'
        header['host'] = 'www.nike.com'
    elif '{countryLangRegion}' in path:
        return
        path = path.replace('{countryLangRegion}', country_lang_region)
        header['host'] = 'store.nike.com'
    else:
        path = f'{host}/{path}'
        header['host'] = 'www.nike.com'

    resp = req(path, header=header)
    if resp == 400:
        logger.warning('path is wrong, the path is {}'.format(path))
        return

    data = json.loads(re.search(pattern, resp).group(1))
    products = data['Threads']['products']

    for product in products.values():
        info = {}
        info['标题'] = product['fullTitle']
        info['货号'] = product['styleColor']
        info['颜色'] = product['colorDescription']
        info['分类'] = product['subTitle']
        info['原价'] = product['fullPrice']
        info['折后价'] = product['currentPrice']

        additional = product.get('additionalInfo')
        if additional:
            limit = re.search(limit_pattern, additional)
            promotion = re.search(promotion_pattern, additional)
            info['是否限购'] = '否' if not limit else '限购{}件'.format(limit.group(1))
            info['是否支持优惠券'] = '否' if promotion else '是'
        else:
            info['是否限购'] = '否'
            info['是否支持优惠券'] = '否'

        try:
            info['折扣率'] = '{:.2%}'.format(int(info['折后价']) / int(info['原价']))
        except:
            logger.error('{} / {} is wrong'.format(info['折后价'], info['原价']))
            info['折扣率'] = ''
        info['更新时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info['新增货号'] = '是'
        info['轮次'] = 0
        # if product['seoProductAvailability'] is True:
        skus, detail = judge_sku(product)
        # print('-->1{}'.format(info))
        for index in range(len(skus)):
            if detail[index] == '有货':
                info['库存'] = 3 + int(random.random() * 7)
                info['尺码'] = skus[index]
                info['是否有货'] = detail[index]
                # print('-->2{}'.format(info))
                try:
                    # with lock:
                    excel.write(info)
                except Exception as exc:
                    print(exc)
                # INFO.append(info)
                # print('-->3{}'.format(len(INFO)))
                logger.error('{} - {} - {}'.format(info['货号'], info['尺码'],
                                                   info['是否有货']))
            else:
                continue


def first_page(path, em):
    resp = req(path, header=header)
    data = json.loads(re.search(pattern, resp).group(1))
    products = data['Wall']['products']

    # for product in products:
    #     if product['cardType'] != 'default':
    #         continue
    #     run_func(get_detail, product['url'])
    path_list = []
    for product in products:
        if product['cardType'] == 'default':
            if '专属定制' in product['subtitle']:
                logger.error('专属定制')
            else:
                path_list.append(product['url'])

    multi_processes(path_list, em)
    logger.info('first page down')
    run_func(last_page, data['Wall']['pageData']['next'], em)


def multi_processes(path_list, em):
    # for path in path_list:
    #     get_detail(path)

    # m = MyManager()
    # m.start()
    # counter = m.excel(0)

    # lock = Lock()

    pool = Pool(8)
    for path in path_list:
        pool.apply_async(
            run_func,
            (
                get_detail,
                path,
                em,
                # lock,
            ))
    pool.close()
    pool.join()


def last_page(path, em):
    resp = req(f'{host}/{path}', header=header)
    data = json.loads(resp)
    path_list = []
    for item in data['objects']:
        if '专属定制' in item['publishedContent']['properties']['subtitle']:
            logger.error('专属定制')
        else:
            path_list.append('cn/t/{}'.format(
                item['publishedContent']['properties']['seo']['slug']))

    multi_processes(path_list, em)

    # try:
    #     get_detail(f'cn/t/{path}')
    # except TypeError:
    #     logger.warning('path is wrong, reget now')
    #     path = item['rollup']['threads'][0]['publishedContent'][
    #         'properties']['seo']['slug']
    #     run_func(get_detail, f'cn/t/{path}')

    logger.info('last page down')
    next_path = data.get('pages').get('next')
    if next_path:
        run_func(last_page, next_path, em)


def main():
    manager = Manager2()
    em = manager.excel()
    em.init_sheet(header=[
        '标题', '货号', '尺码', '颜色', '库存', '分类', '原价', '折后价', '折扣率', '更新时间', '新增货号',
        '是否有货', '是否限购', '是否支持优惠券', '轮次'
    ])
    # excel.init_sheet(header=[
    #     '标题', '货号', '尺码', '颜色', '库存', '分类', '原价', '折后价', '折扣率', '更新时间', '新增货号',
    #     '是否有货', '是否限购', '是否支持优惠券', '轮次'
    # ])

    home_list = [
        'https://www.nike.com/cn/w/mens-shoes-nik1zy7ok',
        'https://www.nike.com/cn/w/womens-shoes-5e1x6zy7ok',
        'https://www.nike.com/cn/w/mens-apparel-6ymx6znik1',
        'https://www.nike.com/cn/w/womens-apparel-5e1x6z6ymx6',
        'https://www.nike.com/cn/w/boys-shoes-1onrazy7ok',
        'https://www.nike.com/cn/w/girls-shoes-3aqegzy7ok',
        'https://www.nike.com/cn/w/boys-apparel-1onraz6ymx6',
        'https://www.nike.com/cn/w/girls-apparel-3aqegz6ymx6',
        'https://www.nike.com/cn/w/mens-accessories-equipment-awwpwznik1',
        'https://www.nike.com/cn/w/womens-accessories-equipment-5e1x6zawwpw'
    ]

    for path in home_list:
        run_func(first_page, path, em)
    # a = time.time()
    # for item in INFO:
    #     run_func(excel.write, item)
    # print(time.time() - a)

    # a = time.time()
    # run_func(em.save)
    # print(time.time() - a)

    run_func(em.save)
    logger.error('save successful')
    time.sleep(300)


req = Query().run
# excel = ExcelOpea()
host = 'https://www.nike.com'
country_lang = 'cn'
country_lang_region = 'https://store.nike.com/cn/zh_cn'
pattern = re.compile(r'window.INITIAL_REDUX_STATE=(.*);</script>')
limit_pattern = re.compile(r'限购.*>([1-9]\d*)<.*')
promotion_pattern = re.compile(r'不参加任何折扣优惠|不适用于任何优惠券')
INFO = []


class MyManager(BaseManager):
    pass


MyManager.register('excel', ExcelOpea)

# a = '\u003Cdiv\u003E\u003Ch2\u003E特别版产品销售规则\u003C\u002Fh2\u003E\u003Cp style=\"margin: 6pt 0cm; line-height: 12.25pt; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E1.此商品每人限购\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E1\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E件，且不适用于任何优惠券\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u002F\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E礼品卡等折扣活动。\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u003Co:p\u003E\u003C\u002Fo:p\u003E\u003C\u002Fspan\u003E\u003C\u002Fp\u003E\n\n\u003Cp style=\"margin: 6pt 0cm; line-height: 12.25pt; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E2.\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E此商品仅支持网上在线支付，且需在商品订单提交后\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E24\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E小时内成功付款。超时订单将被取消。成功付款以本网站确认付款信息为准，您可以通过查询订单状态实时了解是否已成功付款。\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u003Co:p\u003E\u003C\u002Fo:p\u003E\u003C\u002Fspan\u003E\u003C\u002Fp\u003E\n\n\u003Cp style=\"margin: 6pt 0cm; line-height: 12.25pt; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E3.\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E网上在线成功支付需要多方协同，例如您的付款银行、支付及交易平台以及网络接入服务提供商等。自您进行支付后，各方系统需要一定时间进行数据交换直至本网站确认付款成功。\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u003Co:p\u003E\u003C\u002Fo:p\u003E\u003C\u002Fspan\u003E\u003C\u002Fp\u003E\n\n\u003Cp style=\"margin: 6pt 0cm; line-height: 12.25pt; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E4.\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E在此期间，一旦发生网络传输延迟或数据交换堵塞可能会影响您成功付款，因此建议您在订单提交后尽快进行付款，以避免因网络延迟未能成功付款而导致订单取消的情形出现。\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u003Co:p\u003E\u003C\u002Fo:p\u003E\u003C\u002Fspan\u003E\u003C\u002Fp\u003E\n\n\u003Cp style=\"margin: 6pt 0cm; line-height: 12.25pt; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E5.\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E耐克在某些情况下有权单方取消您的订单，如您已进行付款，耐克只需通过原付款平台向您退回您已支付款项，且无需承担其他责任。这些情况具体请见\u003C\u002Fspan\u003E\u003Ca href=\"http:\u002F\u002Fhelp-zh-cn.nike.com\u002Fapp\u002Fanswers\u002Fdetail\u002Farticle\u002Fcancel_qs\"\u003E\u003Cb\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E特别版产品订单取消规则\u003C\u002Fspan\u003E\u003C\u002Fb\u003E\u003C\u002Fa\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E。\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u003Co:p\u003E\u003C\u002Fo:p\u003E\u003C\u002Fspan\u003E\u003C\u002Fp\u003E\n\n\u003Cp style=\"margin: 6pt 0cm; line-height: 12.25pt; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E6.\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E由于不可抗力、传输迟延、耐克网站系统发生故障或遭受第三方攻击及其他耐克无法控制的情形，耐克有权暂时下架或延迟发售此商品。如您已下单购买此商品但因上述原因发生缺货的，您有权取消订单，商城亦有权取消订单，并仅需为您办理退款。\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u003Co:p\u003E\u003C\u002Fo:p\u003E\u003C\u002Fspan\u003E\u003C\u002Fp\u003E\n\n\u003Cp style=\"margin: 6pt 0cm; line-height: 12.25pt; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E7.\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E特别版产品实行\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt;\"\u003E&ldquo;\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E先购先得\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt;\"\u003E&rdquo;\u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E原则，如购买人数众多，您最终有可能因该产品迅速售罄而无法买到该产品。\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u003Co:p\u003E\u003C\u002Fo:p\u003E\u003C\u002Fspan\u003E\u003C\u002Fp\u003E\n\n\u003Cp style=\"margin: 6pt 0cm; line-height: 12.25pt; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E- \u003C\u002Fspan\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E此商品为耐克推出的特别版产品，在您购买此商品前，敬请仔细阅读本网站\u003C\u002Fspan\u003E\u003Ca href=\"http:\u002F\u002Fhelp-zh-cn.nike.com\u002Fapp\u002Fanswers\u002Fdetail\u002Farticle\u002Fterms\u002Fa_id\u002F36483\u002Fp\u002F3897\"\u003E\u003Cb\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E使用条款\u003C\u002Fspan\u003E\u003C\u002Fb\u003E\u003C\u002Fa\u003E\u003Cspan lang=\"ZH-CN\" style=\"font-size: 10.5pt; font-family: 宋体;\"\u003E及上述特别版产品销售规则，如您选择继续通过本网站购买此商品，代表您已同意并接受前述规则。\u003C\u002Fspan\u003E\u003Cspan style=\"font-size: 10.5pt; font-family: proxima_nova, serif;\"\u003E\u003Co:p\u003E\u003C\u002Fo:p\u003E\u003C\u002Fspan\u003E\u003C\u002Fp\u003E\n\u003C\u002Fdiv\u003E'

# b = re.search(limit_pattern, a)
# c = re.search(promotion_pattern, a)

header = {
    'Host': 'www.nike.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    # 'Referer': '',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cookie': get_cookie()
}


class MyManager(BaseManager):
    pass


MyManager.register('excel', ExcelOpea)


def Manager2():
    m = MyManager()
    m.start()
    return m


if __name__ == "__main__":
    freeze_support()
    main()