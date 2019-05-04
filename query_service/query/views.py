from django.http import HttpResponse

from query import request_repair
from django.shortcuts import render

from django.http.response import JsonResponse
import json


def query(request):
    if request.method == 'GET':
        try:
            imei = request.GET.get('imei')
            if imei:
                query_data = request_repair.main(imei)
                print("query_data is {}".format(query_data))
                json_ = {
                    "status": "success",
                    "msg": {
                        "IMEI": imei,
                        "Find My iPhone": "",
                        "FMI STATUS": ""
                    }
                }
                # string = "IMEI: {}\nFind My iPhone: {}\nAnd is the 'Lost' mode active on your device: {}"
                if query_data == 'off':
                    json_["msg"]["Find My iPhone"] = "OFF（关闭）"
                    del json_["FMI STATUS"]
                elif isinstance(query_data, tuple):
                    json_["msg"]["Find My iPhone"] = "ON（开启）"
                    if query_data[-1] == "yes":
                        json_["msg"]["FMI STATUS"] = "LOST（黑）"
                    else:
                        json_["msg"]["FMI STATUS"] = "CLEAN（白）"
                elif query_data == "Invalid serial number":
                    json_ = {"status": "error", "msg": "IMEI 错误"}
                else:
                    return HttpResponse("请重试")
                # return JsonResponse(json_)
                return HttpResponse(
                    json.dumps(json_, ensure_ascii=False),
                    content_type="application/json;charset=utf-8")
            else:
                return HttpResponse("您的输入不合法，请重新输入")
        except:
            return render(request, "query/query_data.html")

    elif request.method == 'POST':
        imei = request.POST.get('imei')

        if imei:
            query_data = request_repair.main()
            if query_data:
                string = "IMEI: {}\nFind My iPhone: {}\nAnd is the 'Lost' mode active on your device: {}"
                return HttpResponse(
                    string.format(imei, query_data[0], query_data[-1]))
            else:
                return HttpResponse("请重试")
        else:
            return HttpResponse("您的输入不合法，请重新输入")
