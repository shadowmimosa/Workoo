# def try_werobot():
#     import werobot
#     pass

# try:
#     b = 1
#     a = b
#     print(a)
# except SyntaxError:
#     print("SyntaxError")
# except NameError:
#     print("NameError")
# else:
#     print("Ok")
# finally:
#     print("Finally")

# print(round(2 - 1.59, 3))

from decimal import Decimal
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        end_time = time.time()
        print("执行函数{}使用了{}秒".format(
            getattr(func, "__name__"), end_time - start_time))
        return f

    return wrapper


@timer
def test_decimal():
    for _ in range(1000000):
        num = '{:.2f}'.format(Decimal('2') - Decimal('1.59'))


@timer
def test_round():
    for _ in range(1000000):
        number = round(2 - 1.59, 2)


@timer
def test_decimal_1():
    for _ in range(1000000):
        num = '{:.2f}'.format(2 - Decimal('1.59'))


@timer
def test_format():
    a = "string"
    for _ in range(1000000):
        string = "string %s" % a


@timer
def test_format_1():
    a = "string"
    for _ in range(1000000):
        string = ""
        string += a


@timer
def test_format_2():
    a = "string"
    for _ in range(1000000):
        string = "string {}".format(a)


@timer
def test_int():
    for _ in range(1000000):
        int("66")


def test_replace():
    string = "IMEI: 355831083320852<br>Model: iPhone 7 256GB Red<br>Model Number: A1660\/A1780<br>Identifier: iPhone9,1<br>Order: MNAD2CH\/A<br>Network: GSM\/CDMA\/LTE<br>Activated: <span style=\"color:green;\">Yes<\/span><br>Purchase Date: 2017-05-11 <sup>Valid<\/sup><br>Repairs & Service Coverage: <span style=\"color:red;\">No<\/span><br>Technical Support: <span style=\"color:red;\">No<\/span><br>Manufacturer: Foxconn"
    string = "IMEI: 357265095019541<br>Find My iPhone: <span style=\"color:green;\">OFF<\/span>"
    string = "IMEI: 357288092352459<br>Find My iPhone: <span style=\"color:red;\">ON<\/span><br>iCloud Status: <span style=\"color:red;\">Lost Mode<\/span>"
    start = time.time()
    string = string.replace("<br>", "\n").replace(
        "Find My iPhone", "找到我的iPhone"
    ).replace('<span style=\"color:red;\">ON<\/span>', "ON （开启）").replace(
        '<span style=\"color:green;\">OFF<\/span>',
        "OFF（关闭）").replace("iCloud Status", "iCloud状态").replace(
            '<span style="color:red;">Lost Mode<\/span>',
            "丢失模式").replace("Model Number", "型号").replace(
                "Model", "型号").replace("Identifier", "类型").replace(
                    "Order", "型号").replace("Network", "网络").replace(
                        "Activated",
                        "已激活").replace("Purchase Date", "购买日期").replace(
                            "Repairs & Service Coverage", "维修和服务范围").replace(
                                "Technical Support", "技术支持").replace(
                                    "Manufacturer", "制造商"
                                ).replace("Foxconn", "富士康").replace(
                                    "<sup>Valid<\/sup>", "有效"
                                ).replace("<sup>", "").replace(
                                    "<\/sup>", ""
                                ).replace(
                                    '<span style="color:green;">Yes<\/span>',
                                    "是").replace(
                                        '<span style="color:red;">No<\/span>',
                                        "否").replace(
                                            '<span style="color:red;">',
                                            "").replace("<\/span>", "")
    a = "SUCCESS{OrderID: 2965307,IMEI: 353844083785828,Result: Model: IPHONE 7 32GB GOLD MM [A1778] [IPHONE9,1]<br>IMEI: 353844083785828<br>Serial Number: C6KSN81PHG7H<br>Purchase Date: 2016-12-12<br>Activation Status: Activated<br>Warranty Status: Out Of Warranty<br>Telephone Technical Support: Expired<br>Repairs and Service Coverage: Expired<br>Valid Purchase Date: Yes<br>AppleCare Eligible: No<br>Registered: Yes<br>Replaced: No<br>Loaner: No<br>Find My iPhone: <font color=008000>OFF</font><br>Carrier: Unlock<br>SIMLock Status: <font color=008000>Unlocked</font>}"
    a = a.split("Result:")[-1]
    # ' Model: IPHONE 7 32GB GOLD MM [A1778] [IPHONE9,1]<br>IMEI: 353844083785828<br>Serial Number: C6KSN81PHG7H<br>Purchase Date: 2016-12-12<br>Activation Status: Activated<br>Warranty Status: Out Of Warranty<br>Telephone Technical Support: Expired<br>Repairs and Service Coverage: Expired<br>Valid Purchase Date: Yes<br>AppleCare Eligible: No<br>Registered: Yes<br>Replaced: No<br>Loaner: No<br>Find My iPhone: <font color=008000>OFF</font><br>Carrier: Unlock<br>SIMLock Status: <font color=008000>Unlocked</font>}'
    a = a.replace("<br>", "\n").replace("Model", "型号").replace(
        "Serial Number",
        "序列号").replace("Valid Purchase Date", "有效购买日期").replace(
            "Purchase Date",
            "购买日期").replace("Activation Status", "激活状态").replace(
                "Warranty Status", "保修状态"
            ).replace("Telephone Technical Support", "电话技术支持").replace(
                "Repairs and Service Coverage", "维修和服务范围").replace(
                    "AppleCare Eligible", "AppleCare符合条件").replace(
                        "Registered", "注册").replace("Replaced", "替换").replace(
                            "Replaced", "替换").replace("Loaner", "借用者").replace(
                                "Find My iPhone", "找到我的iPhone").replace(
                                    "SIMLock Status", "SIMLock状态").replace(
                                        "Repairs and Service Expiration Date",
                                        "维修和服务有效期").replace(
                                            "Repairs and Service Expires In",
                                            "维修和服务到期时间").replace(
                                                "<font color=008000>",
                                                "").replace("</font>",
                                                            "").replace(
                                                                "}", "")

    # print(a)
    # print(start)
    # print(time.time() - start)
    # print(string)
    data = {
        "imei": "IMEI",
        "sn": "序列号",
        "description": "型号（整合）",
        "model": "型号",
        "storage": "容量",
        "color": "颜色",
        "type": "网络类型",
        "number": "网络型号（参考）",
        "identifier": "产品类型",
        "order": "零件编号（参考）",
        "network": "支持网络（参考）",
        "status": "设备状态（normal、refurbished）",
        "activated": "激活状态",
        "purchase": {
            "date": "激活日期（预估购买日期）",
            "validated": "有效购买日期，true=>是（已验证）、false=>未验证",
        },
        "coverage": "保修结束日期或expired（已过期）、active（未过期）",
        "daysleft": "保修剩余（天）",
        "support": "技术支持或expired（已过期）、active（有效）",
        "applecare": "是否延保",
        "loaner": "借出设备，Y=>是、N=>否",
        "manufacture": {
            "date": "生产日期",
            "factory": "产地",
        },
        "manufacturer": "制造商（生产工厂）",
        "img": "设备图片",
    }

    a = data.keys()
    print(a)

def run_html():
    from bs4 import BeautifulSoup
    import codecs
    import requests
    import wget
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    target = "http://www.biqukan.com/1_1094/5403177.html"
    filenanme = wget.download(url=target)
    with open(filenanme,'r',encoding='gbk') as f:
        bf = BeautifulSoup(f,features="html.parser")
        texts = bf.find_all('div',class_='showtxt')
        print(texts)


if __name__ == "__main__":
    run_html()
    # test_replace()
    # test_int()
    # test_format()
    # test_format_1()
    # test_format_2()
    # test_round()
    # test_decimal()
    # test_decimal_1()