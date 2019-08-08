import requests

zhima_url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&pack=55163&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="


def init_zhima():
    resp = requests.get(zhima_url).text
    a = resp.split(":")[0]
    b = resp.split(":")[-1].replace("\r\n", "")

    proxyMeta = "http://%(host)s:%(port)s" % {
        "host": resp.split(":")[0],
        "port": resp.split(":")[-1].replace("\r\n", ""),
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    resp = requests.get("http://www.baidu.com", proxies=proxies)

    print(proxies)


init_zhima()