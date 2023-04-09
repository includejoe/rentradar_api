from django.contrib import admin

from . import models


# Register your models here.
class UserReview(admin.ModelAdmin):
    list_display = ("id", "body", "created_at")


admin.site.register(models.UserReview, UserReview)


class RentalReview(admin.ModelAdmin):
    list_display = ("id", "body", "created_at")


admin.site.register(models.RentalReview, RentalReview)
