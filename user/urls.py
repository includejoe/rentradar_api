from django.urls import path
from .views import retrieve_update_user_view, get_public_user_details_view

app_name = "user"

urlpatterns = [
    path("", retrieve_update_user_view, name="retrieve_update_user"),
    path(
        "details/<str:user_id>/",
        get_public_user_details_view,
        name="get_public_user_details",
    ),
]
