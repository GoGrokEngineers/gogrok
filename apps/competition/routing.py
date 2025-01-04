from django.urls import re_path
from apps.competition.consumers import CompetitionRoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/waiting-room/(?P<comp_uid>\w+)/', CompetitionRoomConsumer.as_asgi()),
]
