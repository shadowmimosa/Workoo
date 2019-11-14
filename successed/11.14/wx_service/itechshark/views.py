from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.db.utils import ProgrammingError
import hashlib
import json
import time

from .utils.main import CheckImei


def magic_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        over_time = end_time - start_time
        print("The function {} run time is {}".format(func.__name__,
                                                      over_time))
        if over_time < 6:
            time.sleep(6.5 - over_time)
        
        return res

    return wrapper


@csrf_exempt
@magic_time
def check_imei(request):
    """
    """
    if request.method == "GET":
        imei = request.GET.get("imei")
        msg = CheckImei().run(imei)
        # try:
        #     msg = CheckImei().run(imei)
        # except Exception as exc:
        #     print(exc)
        #     msg = {"status": "failed"}

        return HttpResponse(
            json.dumps(msg, ensure_ascii=False),
            content_type="application/json;charset=utf-8")
