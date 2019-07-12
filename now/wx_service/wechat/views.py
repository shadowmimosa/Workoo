from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import hashlib
import json
import time

# from wechat.analysis import Analysis
from .analysis import Analysis

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
        toWxData = analysisObj.prase(smart_str(request.body))
        print(toWxData)
        return HttpResponse(smart_str(toWxData))
