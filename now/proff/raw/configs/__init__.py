HEADERS = """
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cache-Control: no-cache
Host: www.proff.no
Pragma: no-cache
Referer: https://www.proff.no/laglister?i=p47431&samplerFilter=true
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36
"""

USER_AGENT = [
    # ie
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; '
    'SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)',
    # msie
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0;'
    ' .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0;'
    ' Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    # opera
    'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62',
    # chrome
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
    # google
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML,'
    ' like Gecko) Chrome/32.0.1664.3 Safari/537.36',
    # google chrome
    'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    # firefox
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
    # ff
    'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0',
    # safari
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP)'
    ' AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27'
]

# 搜索条件
PARAMS = {
    'i': 'p16851',
    'phone': 'false',
    'email': 'false',
    'address': 'false',
    'view': 'json'
}
