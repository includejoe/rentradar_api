from django.urls import path
from .views import (
    create_user_review_view,
    get_user_reviews_view,
    delete_user_review_view,
    create_property_review_view,
    get_property_reviews_view,
    delete_property_review_view,
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
    path(
        "property/create/", create_property_review_view, name="create_property_review"
    ),
    path(
        "property/all/<str:property_id>/",
        get_property_reviews_view,
        name="get_property_reviews",
    ),
    path(
        "property/delete/<str:review_id>/",
        delete_property_review_view,
        name="delete_property_review",
    ),
]
