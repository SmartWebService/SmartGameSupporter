from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/sgs/RPS/(?P<type>[^/]+)/(?P<game_code>[^/]+)/(?P<username>[^/]+)/(?P<sessionKey>[^/]+)/$', consumers.RPSConsumer),
    # url(r'^ws/sgs/RPS/(?P<type>[^/]+)/(?P<game_code>[^/]+)/(?P<sessionKey>[^/]+)/$', consumers.RPSConsumer),

    # url(r'^ws/sgs/five-poker/(?P<type>[^/]+)/(?P<game_code>[^/]+)/(?P<username>[^/]+)/(?P<sessionKey>[^/]+)/$', consumers.FivePokerConsumer),
    # url(r'^ws/sgs/five-poker/(?P<type>[^/]+)/(?P<game_code>[^/]+)/(?P<sessionKey>[^/]+)/$', consumers.FivePokerConsumer),

    # url(r'^ws/sgs/indian-poker/(?P<type>[^/]+)/(?P<game_code>[^/]+)/(?P<username>[^/]+)/(?P<sessionKey>[^/]+)/$', consumers.IndianPokerConsumer),
    # url(r'^ws/sgs/indian-poker/(?P<type>[^/]+)/(?P<game_code>[^/]+)/(?P<sessionKey>[^/]+)/$', consumers.IndianPokerConsumer),
]