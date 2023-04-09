import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    title = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    category = models.CharField(
        max_length=64, choices=CATEGORY_CHOICES, blank=False, null=False
    )
    rate = models.CharField(max_length=128, blank=False, null=False)
    lease_term = models.CharField(max_length=255, blank=False, null=False)
    lease_cost = models.CharField(max_length=128, blank=False, null=False)
    image1 = models.URLField(blank=False, null=False)
    image2 = models.URLField(blank=False, null=False)
    image3 = models.URLField(blank=False, null=False)
    image4 = models.URLField(blank=False, null=False)
    image5 = models.URLField(blank=False, null=False)
    image6 = models.URLField(null=True, blank=True)
    image7 = models.URLField(null=True, blank=True)
    image8 = models.URLField(null=True, blank=True)
    image9 = models.URLField(null=True, blank=True)
    image10 = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
