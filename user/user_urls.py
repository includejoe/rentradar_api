from django.urls import path
from .views import (
    user_details_view,
    public_user_details_view,
    rate_user_view,
    user_kyc_view,
)

app_name = "user"

urlpatterns = [
    path("", user_details_view, name="user_details"),
    path(
        "public/<str:email>/",
        public_user_details_view,
        name="public_user_details",
    ),
    path("rate/<str:email>/", rate_user_view, name="rate-user"),
    path("kyc/", user_kyc_view, name="user-kyc"),
]
