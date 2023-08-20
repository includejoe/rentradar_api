from django.urls import path
from .views import (
    create_rental_view,
    get_all_rentals_view,
    get_user_rentals_view,
    rental_detail_view,
    update_rental_view,
    delete_rental_view,
    filter_rentals_view,
)

app_name = "rental"

urlpatterns = [
    path("all/", get_all_rentals_view, name="all_rentals"),
    path("create/", create_rental_view, name="create_rental"),
    path("details/<str:rental_id>/", rental_detail_view, name="rental_details"),
    path("update/<str:rental_id>/", update_rental_view, name="update_rental"),
    path("delete/<str:rental_id>/", delete_rental_view, name="delete_rental"),
    path("user/<str:user_id>/", get_user_rentals_view, name="user_rentals"),
    path("filter/", filter_rentals_view, name="filter_rentals"),
]
