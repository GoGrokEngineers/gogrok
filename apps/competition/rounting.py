from django.urls import path
from .consumers import CompetitionRoomConsumer

websocket_urlpatterns = [
    path('v2/ws/waiting-room/<str:comp_pin>/', CompetitionRoomConsumer.as_asgi()),
]
