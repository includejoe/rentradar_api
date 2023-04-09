from django.contrib import admin

from . import models


# Register your models here.
class User(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "phone",
        "gender",
        "user_type",
        "user_status",
        "is_verified",
        "rating",
    )


admin.site.register(models.User, User)
