from django.contrib import admin

from . import models


# Register your models here.
class User(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
        "phone",
        "gender",
        "user_type",
        "user_status",
        "rating",
    )


class Rating(admin.ModelAdmin):
    list_display = ("id", "value")


class UserKyc(admin.ModelAdmin):
    list_display = ("id", "verified", "created_at")


admin.site.register(models.User, User)
admin.site.register(models.UserKyc, UserKyc)
admin.site.register(models.Rating, Rating)
