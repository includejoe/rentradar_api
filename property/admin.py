from django.contrib import admin

from . import models

# Register your models here.
class Property(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "num_of_rooms",
        "location",
        "lease_term_in_months",
        "is_lease_term_negotiable",
        "rate",
        "is_rate_negotiable",
        "is_furnished",
        "is_self_contain",
        "total_lease_cost",
    )


admin.site.register(models.Property, Property)
