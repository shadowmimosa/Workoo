from django.urls import path
from django.views.generic import TemplateView
from itechshark import views

app_name = 'itechshark'

urlpatterns = [
    path('query/', views., name='query'),

]
