from rest_framework import serializers
from django.utils import timezone

from .models import User, Rating


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "bus_name", "profile_image", "is_verified", "user_type"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "bus_name",
            "location",
            "password",
            "phone",
            "gender",
            "dob",
            "id_card_image",
            "profile_image",
            "user_type",
            "rating",
            "is_verified",
            "user_status",
            "created_at",
        ]

        read_only_fields = ["id", "created_at" "full_name", "email"]

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.updated_at = timezone.now
        instance.save()

        return instance


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "bus_name",
            "phone",
            "gender",
            "location",
            "rating",
            "created_at",
            "is_verified",
            "profile_image",
            "user_type",
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "user_rated", "rater", "value")
        read_only_fields = ("id", "user_rated", "rater")
