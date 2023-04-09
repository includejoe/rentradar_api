import uuid
from django.db import models
from django.utils import timezone

from user.models import User


# Create your models here.
class Rental(models.Model):
    CATEGORY_CHOICES = (
        ("real-estate", "real-estate"),
        ("vehicles", "vehicles"),
        ("event-supplies", "event-supplies"),
        ("fashion", "fashion"),
        ("recreational", "recreational"),
        ("sports", "sports"),
        ("electronics", "electronics"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES)
    rate = models.DecimalField(max_digits=15, decimal_places=2)
    total_lease_cost = models.DecimalField(max_digits=15, decimal_places=2)
    image1 = models.URLField()
    image2 = models.URLField()
    image3 = models.URLField()
    image4 = models.URLField()
    image5 = models.URLField()
    image6 = models.URLField(null=True, blank=True)
    image7 = models.URLField(null=True, blank=True)
    image8 = models.URLField(null=True, blank=True)
    image9 = models.URLField(null=True, blank=True)
    image10 = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
