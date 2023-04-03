from django.urls import path
from .views import (
    post_property_view,
    get_user_properties_view,
    property_detail_view,
    get_all_properties_view,
    filter_properties_view,
)

app_name = "property"

urlpatterns = [
    path("all/", get_all_properties_view, name="all_properties"),
    path("post/", post_property_view, name="post_properties"),
    path("detail/<str:property_id>/", property_detail_view, name="property_detail"),
    path("user/<str:user_id>/", get_user_properties_view, name="user_properties"),
    path("filter/", filter_properties_view, name="filter_properties"),
]
