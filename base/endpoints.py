from django.urls import path, include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    # path("user/", include("user.urls")),
    # path("property/", include("property.urls")),
    # path("review/", include("review.urls")),
]
