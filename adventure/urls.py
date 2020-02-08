from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('players', api.players),
    url('get', api.get),
    url('drop', api.drop),
    url('look', api.look),
    url('inventory', api.inventory),
    url('scan', api.scan),
    url('steal', api.steal),
]