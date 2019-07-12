from django.urls import path
from wechat import views

app_name = 'wechat'

urlpatterns = [path('', views.check_signature, name='query')]