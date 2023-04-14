from django.urls import path
from .views import (
    start_conversation_view,
    get_conversation_view,
    get_conversation_list_view,
)

app_name = "chat"

urlpatterns = [
    path(
        "start/<str:receiver_id>/", start_conversation_view, name="start_conversation"
    ),
    path("<str:conversation_id>/", get_conversation_view, name="get_conversation"),
    path("", get_conversation_list_view, name="get_conversation_list"),
]
