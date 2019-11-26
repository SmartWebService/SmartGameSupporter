from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/sgs/(?P<type>[^/]+)/(?P<game_code>[^/]+)/(?P<username>[^/]+)/(?P<sessionKey>[^/]+)/$', consumers.SGSConsumer),
    url(r'^ws/sgs/(?P<type>[^/]+)/(?P<game_code>[^/]+)/(?P<sessionKey>[^/]+)/$', consumers.SGSConsumer),
]