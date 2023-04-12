from django.urls import path, include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("user/", include("user.urls")),
    path("rental/", include("rental.urls")),
    path("review/", include("review.urls")),
    path("chat/", include("chat.urls")),
]
