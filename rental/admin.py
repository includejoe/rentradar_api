from django.contrib import admin

from . import models


# Register your models here.
class Rental(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "location",
        "rate",
        "lease_term",
        "lease_cost",
        "created_at",
    )


admin.site.register(models.Rental, Rental)
