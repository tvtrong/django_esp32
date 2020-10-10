#from django.conf.urls import url
from django.urls import re_path, path
from . import consumers
websocket_urlpatterns = [
    path('ws/dht11/', consumers.DHT11LatestConsumer, name='ws_dht11latest')
]
