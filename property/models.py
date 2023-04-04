import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from user.models import User

# Create your models here.
class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    num_of_rooms = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )
    location = models.CharField(max_length=255)
    lease_term_in_months = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )
    is_lease_term_negotiable = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=15, decimal_places=2)
    is_rate_negotiable = models.BooleanField(default=False)
    is_furnished = models.BooleanField(default=False)
    is_self_contain = models.BooleanField(default=False)
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

    @property
    def total_lease_cost(self):
        return self.lease_term_in_months * self.rate

    class Meta:
        ordering = ["-created_at"]
