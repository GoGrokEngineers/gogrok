from django.urls import re_path
from .consumers import CompetitionRoomConsumer

websocket_urlpatterns = [
    re_path(r'^v2/ws/waiting-room/(?P<comp_uid>\w+)/$', CompetitionRoomConsumer.as_asgi()),
]
