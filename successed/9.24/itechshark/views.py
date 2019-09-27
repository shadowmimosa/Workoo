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


@csrf_exempt
def update_count(request):
    """
    """
    if request.method == "GET":
        counts = request.GET.get("imei")
        try:
            msg = CheckImei().run("359168077743765")
        except Exception as exc:
            print(exc)
            msg = {"status": "failed"}

        return HttpResponse(
            json.dumps(msg, ensure_ascii=False),
            content_type="application/json;charset=utf-8")
