from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import hashlib
import json
import time

# from wechat.analysis import Analysis
from .utils.analysis import Analysis
from .utils.service import WxPay
from .utils.service import oauth_wx
from .utils.set_button import SetButton
from .utils.common import monthly_price, free_time, get_event

#微信的介入验证是GET方法
#微信正常的收发消息是POST方法


@csrf_exempt
def check_signature(request):
    if request.method == "GET":
        print("welcome wx")
        #下面这四个参数是在接入时，微信的服务器发送过来的参数
        signature = request.GET.get('signature', None)
        #print(signature)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        #这个token是我们自己来定义的，并且这个要填写在开发文档中的Token的位置
        token = 'aifengchaxun123'
        #把token，timestamp, nonce放在一个序列中，并且按字符排序
        hashlist = [token, timestamp, nonce]
        hashlist.sort()

        #将上面的序列合成一个字符串
        hashstr = ''.join([s for s in hashlist])

        #通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
        s1 = hashlib.sha1()
        s1.update(hashstr.encode("utf8"))
        hashstr = s1.hexdigest()
        #print(hashstr)
        #把我们生成的字符串和微信服务器发送过来的字符串比较，
        #如果相同，就把服务器发过来的echostr字符串返回去
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("field")

    elif request.method == "POST":
        print("POST请求")
        analysisObj = Analysis(smart_str(request.body))
        toWxData = analysisObj.reply()
        print(toWxData)
        return HttpResponse(smart_str(toWxData))


@csrf_exempt
def wx_pay(request):
    if request.method == "GET":
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)
        openid = oauth_wx(code)
        ret = {"openid": openid}
        # ret = {"openid": "openid"}
        return render(request, 'wechat/home.html', ret)

        # ret = {"openid": "omFm91TlajGX2aYF9mDptN623vPM"}
        # return render(request, 'wechat/home.html', ret)
        pass
    elif request.method == "POST":
        print(request.body)
        print(request.POST)
        openid = request.POST.get("openId")
        fee = request.POST.get("totalFee")

        data = WxPay(openid, fee).unified_order()
        # data = {"status": 1}

        return HttpResponse(
            json.dumps(data, ensure_ascii=False),
            content_type="application/json;charset=utf-8")


@csrf_exempt
def result(request):
    if request.method == "GET":
        return HttpResponse("666")
    elif request.method == "POST":
        print("result is {}".format(request.body))
        print(request.POST)

        data = WxPay().trans_xml_to_dict(request.body)
        if data["return_code"] == "SUCCESS":
            out_trade_no = data["out_trade_no"]
            openid = data["openid"]
            fee = data["total_fee"]
            WxPay().update_order(out_trade_no, openid, fee)

        else:
            pass
        toWxData = WxPay().trans_dict_to_xml({
            "return_code": "SUCCESS",
            "return_msg": "OK"
        })
        return HttpResponse(smart_str(toWxData))


@csrf_exempt
def judge(request):
    return TemplateView.as_view(
        template_name='MP_verify_eCuMRMZfC1i8hSsw.txt',
        content_type='text/plain')


@csrf_exempt
def change_price(request):
    """修改包月金额
    
    `example`

        /wx/price?item=month_1&price=50
        /wx/price?item=month_3&price=100
        /wx/price?item=month_6&price=200
        /wx/price?item=month_imei&price=80

    """
    item = request.GET.get("item")
    price = request.GET.get("price")

    if item in ["month_1","month_3","month_6","month_imei"]:
        return HttpResponse(
            json.dumps(monthly_price(item=item, price=price), ensure_ascii=False),
            content_type="application/json;charset=utf-8")
    else:
        return HttpResponse(
            json.dumps(get_event(item=item, price=price), ensure_ascii=False),
            content_type="application/json;charset=utf-8")


def change_count(request):
    """修改每天免费次数
    
    `example`

        /wx/free?count=1

    """
    count = request.GET.get("count")
    return HttpResponse(
        json.dumps(free_time(sign=count), ensure_ascii=False),
        content_type="application/json;charset=utf-8")


@csrf_exempt
def update_balance(request):
    pass


@csrf_exempt
def wx_pay_(request):
    if request.method == "POST":
        print(request.body)
        print(request.POST)

        openid = request.POST.get("openId")
        id_ = request.POST.get("id")
        fee = 0
        if id_ == "recharge_0":
            fee = request.POST.get("sn")
            order_type = 1
        elif "month" in id_:
            if id_ == "month_1":
                order_type = 21
            elif id_ == "month_3":
                order_type = 22
            elif id_ == "month_6":
                order_type = 23
            elif id_ == "month_imei":
                order_type = 24
            fee = monthly_price(id_)
        else:
            if id_ == "recharge_200":
                order_type = 31
            elif id_ == "recharge_500":
                order_type = 32
            elif id_ == "recharge_1000":
                order_type = 33
            fee = int(id_.replace("recharge_", ""))
        print("openid is {}".format(openid))
        print(id_, fee, openid)

        data = WxPay(openid, fee, order_type).unified_order()

        return HttpResponse(
            json.dumps(data, ensure_ascii=False),
            content_type="application/json;charset=utf-8")


def set_button(request):
    SetButton().button()
    return HttpResponse("666")


def update(request):
    openid = request.GET.get("openid")
    WxPay().update_order(
        out_trade_no="36671BC0AE00FFA61B7B393092AE4BCA",
        openid=openid,
        fee=100)

    return HttpResponse("777")


def wx_page(request):
    if request.method == "GET":
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)
        # openid = oauth_wx(code)
        # ret = {"openid": openid}
        ret = monthly_price()
        ret["openid"] = "omFm91TlajGX2aYF9mDptN623vPM"
        return render(request, 'wechat/wxRecharge.html', ret)
