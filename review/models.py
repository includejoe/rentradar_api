import uuid
from django.db import models
from django.utils import timezone

from user.models import User
from property.models import Property

# Create your models here.
class UserReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reviews_written"
    )
    user_reviewed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]


class PropertyReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="property_reviews_written"
    )
    property_reviewed = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="reviews"
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]
