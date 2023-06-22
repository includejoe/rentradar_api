from django.urls import path, include

urlpatterns = [
    path("auth/", include("user.auth_urls")),
    path("user/", include("user.user_urls")),
    path("rental/", include("rental.urls")),
    path("review/", include("review.urls")),
    path("chat/", include("chat.urls")),
]
