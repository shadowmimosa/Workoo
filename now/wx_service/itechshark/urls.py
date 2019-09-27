from django.urls import path
from django.views.generic import TemplateView
from itechshark import views

app_name = 'itechshark'

urlpatterns = [
    path('', views.check_imei, name='query'),

]
