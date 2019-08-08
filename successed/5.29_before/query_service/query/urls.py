from django.urls import path
from query import views

app_name = 'background'

urlpatterns = [path('query/', views.query, name='query')]
