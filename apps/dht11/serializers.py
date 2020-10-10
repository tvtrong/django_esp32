from apps.dht11.models import DHT11
from rest_framework import serializers


class DHT11Serializer(serializers.HyperlinkedModelSerializer):
    #api_key = serializers.HiddenField(default=None)

    class Meta:
        model = DHT11
        fields = [
            'timestamp',
            'temperature',
            'humidity',
            # 'api_key'
        ]
