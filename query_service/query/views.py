from django.http import HttpResponse

from query import request_repair
from django.shortcuts import render


def query(request):
    if request.method == 'GET':
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
