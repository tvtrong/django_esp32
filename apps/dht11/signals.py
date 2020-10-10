from django.dispatch import Signal

new_dht11 = Signal(providing_args=['temperature', 'humidity'])
