from os.path import abspath

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from apps.dht11 import views

router = DefaultRouter()  # router
router.register('list', views.DHT11ViewSet)  # router
app_name = "dht11"
urlpatterns = [
    path('api/', include(router.urls), name='rest_api'),  # router
    path('api/lates/', views.dht11_lates, name='lates'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.dht11, name='dht11'),
    path('to_xlsx/', views.dht11_to_xlsx, name='to_xlsx'),
    path('form/', views.form, name='form'),
]
'''
1.  urlpatterns += router.urls
2.  url(r'^', include(router.urls)),
3.  với không gian tên ứng dụng : 
    url(r'^api/', include((router.urls, 'dht11'))),
4.  Hoặc cả không gian tên ứng dụng và phiên bản:
    url(r'^api/', include((router.urls, 'dht11'), namespace='instance_name')),
'''
