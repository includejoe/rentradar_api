from django.urls import path
from .views import user_details_view, public_user_details_view, rate_user_view

app_name = "user"

urlpatterns = [
    path("", user_details_view, name="user_details"),
    path(
        "public/<str:user_id>/",
        public_user_details_view,
        name="public_user_details",
    ),
    path("rate/<str:user_id>/", rate_user_view, name="rate"),
]
