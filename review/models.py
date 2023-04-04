import uuid
from django.db import models
from django.utils import timezone

from user.models import User

# Create your models here.
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_written"
    )
    user_reviewed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]
