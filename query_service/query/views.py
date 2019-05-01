from django.http import HttpResponse

from query import request_repair
from django.shortcuts import render

from django.http.response import JsonResponse


def query(request):
    if request.method == 'GET':
        # try:
        #     imei = request.GET.get('imei')
        #     if imei:
        #         query_data = request_repair.main()
        #         json_ = {"IMEI": imei, "Find My iPhone": "", "FMI STATUS": ""}
        #         # string = "IMEI: {}\nFind My iPhone: {}\nAnd is the 'Lost' mode active on your device: {}"
        #         if query_data == 'off':
        #             json_["Find My iPhone"] = "off"
        #             del json_["FMI STATUS"]
        #         elif isinstance(query_data,tuple):
        #             json_["Find My iPhone"] = "ON"
        #             if query_data[-1] == "yes":
        #                 json_["FMI STATUS"] = "LOST"
        #             else:
        #                 json_["FMI STATUS"] = "CLEAN"
        #         else:
        #             return HttpResponse("请重试")
        #         return JsonResponse(json_)
        #     else:
        #         return HttpResponse("您的输入不合法，请重新输入")
        # except:
        #     return render(request, "query/query_data.html")
        imei = request.GET.get('imei')
        if imei:
            query_data = request_repair.main()
            json_ = {"IMEI": imei, "Find My iPhone": "", "FMI STATUS": ""}
            # string = "IMEI: {}\nFind My iPhone: {}\nAnd is the 'Lost' mode active on your device: {}"
            if query_data == 'off':
                json_["Find My iPhone"] = "OFF（关闭）"
                del json_["FMI STATUS"]
            elif isinstance(query_data, tuple):
                json_["Find My iPhone"] = "ON（开启）"
                if query_data[-1] == "yes":
                    json_["FMI STATUS"] = "LOST（黑）"
                else:
                    json_["FMI STATUS"] = "CLEAN（白）"
            else:
                return HttpResponse("请重试")
            return JsonResponse(json_)
        else:
            return HttpResponse("您的输入不合法，请重新输入")
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
