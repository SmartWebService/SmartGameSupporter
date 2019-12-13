from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/sgs/RPS/(?P<sessionKey>[^/]+)/$', consumers.RPSConsumer),
    url(r'^ws/sgs/bomb/(?P<sessionKey>[^/]+)/$', consumers.BombConsumer),
    # url(r'^ws/sgs/five-poker/(?P<sessionKey>[^/]+)/$', consumers.FivePokerConsumer),
    # url(r'^ws/sgs/indian-poker/(?P<sessionKey>[^/]+)/$', consumers.IndianPokerConsumer),
]