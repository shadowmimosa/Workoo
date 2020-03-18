# 请以该网址为目标网站 ：https://cuiqingcai.com/8947.html#comments ，
# 使用urllib库中的相应方法，发送请求，
# 并使用函数调用的方法，输出网页源代码，
# 同时，再建立一个函数，使用urllib库中的parse库，输出解析的url结果。
# 要求使用urllib中的error模块成功捕获请求中的超时异常问题。
# 使用函数的形式编写相应的代码。将代码和结果截图提交。

import urllib
import socket
import urllib.request


def parser_url():
    resp = urllib.parse.urlparse(url)
    print(resp.scheme, resp.netloc, resp.path, resp.params, resp.query)


def get_url():
    try:
        resp = urllib.request.urlopen(url)
    except urllib.error.URLError:
        print('网络错误')
    except urllib.error.HTTPError:
        print('请求错误')
    except socket.timeout:
        print('请求超时')
    else:
        print(resp.read().decode('utf-8'))


if __name__ == "__main__":
    url = 'https://cuiqingcai.com/8947.html#comments'
    get_url()
    parser_url()