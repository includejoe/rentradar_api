from django.contrib import admin

from . import models

# Register your models here.
class User(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "gender",
        "id_card_image",
        "user_type",
        "is_verified",
        "agent_fee",
        "agent_rating",
    )


admin.site.register(models.User, User)
