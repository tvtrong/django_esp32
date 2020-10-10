from django.apps import AppConfig


class Dht11Config(AppConfig):
    name = 'dht11'

    def ready(self):
        import apps.dht11.signals
