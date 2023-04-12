from django.urls import re_path

from .consumers import chat_consumer_asgi

websocket_urlpatterns = [re_path(r"ws/chat/(?P<room_name>\w+)/$", chat_consumer_asgi)]
