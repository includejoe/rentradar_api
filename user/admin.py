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
        "is_verified",
        "agent_fee",
        "agent_rating",
    )


admin.site.register(models.User, User)
