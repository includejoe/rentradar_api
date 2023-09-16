from django.contrib import admin

from . import models


# Register your models here.
class User(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "phone",
        "gender",
        "user_type",
        "user_status",
        "is_verified",
        "rating",
    )


admin.site.register(models.User, User)


class Rating(admin.ModelAdmin):
    list_display = ("id", "value")


admin.site.register(models.Rating, Rating)
