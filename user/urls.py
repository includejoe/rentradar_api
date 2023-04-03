from django.urls import path
from .views import retrieve_update_user_view

app_name = "user"

urlpatterns = [path("", retrieve_update_user_view, name="retrieve_update_user")]
