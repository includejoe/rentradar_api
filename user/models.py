import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        bus_name,
        email,
        gender,
        dob,
        phone,
        user_type=1,
        password=None,
        is_superuser=False,
        is_staff=False,
    ):
        if not email:
            raise ValueError("User must have an email")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.bus_name = bus_name
        user.gender = gender
        user.dob = dob
        user.phone = phone
        user.user_type = user_type
        user.set_password(password)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.save()

        return user

    def create_superuser(
        self, first_name, last_name, email, gender, dob, phone, password
    ):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            dob=dob,
            phone=phone,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    bus_name = models.CharField(max_length=128, null=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=128, default="+233")
    gender = models.CharField(max_length=56, default="other")
    dob = models.DateField(null=True)
    location = models.CharField(max_length=255)
    id_card_image = models.URLField(null=True, blank=True)
    profile_image = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    user_type = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3),
        ],
    )
    user_status = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "dob", "gender", "phone"]

    objects = UserManager()

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def clean(self):
        if self.user_type == 1:
            if self.rating is not None:
                raise ValidationError(
                    {"rating": "This field must be null for a user of type 1"}
                )

    class Meta:
        ordering = ["-created_at"]
