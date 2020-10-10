from apps.dht11.models import DHT11
from apps.dht11.serializers import DHT11Serializer
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings


class DHT11LatestConsumer(WebsocketConsumer):
    def connect(self):
        # Join dht11_latest group
        async_to_sync(self.channel_layer.group_add)(
            settings.DHT11_GROUP_NAME,
            self.channel_name
        )
        self.accept()
        print(
            f"---> kết nối từ {self.scope['client'][0]} cổng {self.scope['client'][1]}")

    def disconnect(self, close_code):
        # Leave dht11_latest group
        async_to_sync(self.channel_layer.group_discard)(
            settings.DHT11_GROUP_NAME,
            self.channel_name
        )
        self.close()
        print(
            f"đã đóng websocket với {self.scope['client'][0]} mã {close_code}")

    # Receive data from WebSocket
    def receive(self, text_data):
        client_ = json.loads(text_data)
        # Send data to dht11latest group
        async_to_sync(self.channel_layer.group_send)(
            settings.DHT11_GROUP_NAME,
            {
                'type': 'dht11.msg',
                'msg': client_
            }
        )
    # Receive data from dht11latest group

    def dht11_msg(self, event):
        # Send data to WebSocket
        # Send a data down to the client
        data = event['msg']
        dht11_lates = DHT11.objects.latest('timestamp')
        dht11_latest_serializer = DHT11Serializer(dht11_lates)
        dht11_lates = dht11_latest_serializer.data
        if data['dht11'] and data['dht11']['temperature'] != 0:
            msg = {
                "dht11": data['dht11'],
                "led": data["led"]
            }
        else:
            msg = {
                "dht11": dht11_lates,
                "led": data["led"]
            }
        self.send(text_data=json.dumps(msg))
