from django.urls import path
from django.views.generic import TemplateView
from wechat import views

app_name = 'wechat'

urlpatterns = [
    path('', views.check_signature, name='query'),
    # path('pay/', views.wx_pay, name='pay'),
    path('pay/', views.wx_pay_, name='pay'),
    path('pay/result/', views.result, name='result'),
    path('MP_verify_PpMVUMPN2L1lEYkX.txt', views.judge),
    path('price', views.change_price),
    path('free', views.change_count),
    path('set_button', views.set_button),
    path('insert', views.update),
    path('page', views.wx_page),
]
# path(
#     'MP_verify_PpMVUMPN2L1lEYkX.txt',
#     TemplateView.as_view(
#         template_name='MP_verify_eCuMRMZfC1i8hSsw.txt',
#         content_type='text/plain'))
