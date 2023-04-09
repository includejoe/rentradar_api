from django.urls import path
from .views import (
    create_user_review_view,
    get_user_reviews_view,
    delete_user_review_view,
    create_rental_review_view,
    get_rental_reviews_view,
    delete_rental_review_view,
)

app_name = "review"

urlpatterns = [
    path("user/create/", create_user_review_view, name="create_user_review"),
    path("user/all/<str:user_id>/", get_user_reviews_view, name="get_user_reviews"),
    path(
        "user/delete/<str:review_id>/",
        delete_user_review_view,
        name="delete_user_review",
    ),
    path("rental/create/", create_rental_review_view, name="create_rental_review"),
    path(
        "rental/all/<str:rental_id>/",
        get_rental_reviews_view,
        name="get_rental_reviews",
    ),
    path(
        "rental/delete/<str:review_id>/",
        delete_rental_review_view,
        name="delete_rental_review",
    ),
]
