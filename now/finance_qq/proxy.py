from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    return
    if "quote.json" in flow.request.pretty_url:
        with open("/Users/zhaitiantian3/Public/mock2.json") as f:
            flow.response = http.HTTPResponse.make(
                200, f.read(), {"Content-Type": "application/json"})


def response(flow):
    response = flow.response
    request = flow.request

    url = 'https://bisheng.tenpay.com/fcgi-bin/xg_plate_stocks.fcgi'
    if request.url.startswith(url):
        with open('rank2.txt', 'a', encoding='utf-8') as fn:
            fn.write(response.text)
            fn.write('\n')
