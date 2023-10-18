from django.urls import re_path

from .consumers import chat_consumer_asgi

websocket_urlpatterns = [
    re_path(
        r"^ws/chat/(?P<conversation_id>[^/]+)/(?P<sender_id>[^/]+)/$",
        chat_consumer_asgi,
    )
]
