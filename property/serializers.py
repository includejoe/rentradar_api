from rest_framework import serializers
from django.utils import timezone

from .models import Property
from user.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "profile_image", "is_verified", "user_type"]


class PropertySerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = Property
        fields = [
            "id",
            "user",
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
            "image1",
            "image2",
            "image3",
            "image4",
            "image5",
            "image6",
            "image7",
            "image8",
            "image9",
            "image10",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "user", "created_at", "total_lease_cost"]

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.updated_at = timezone.now
        instance.save()

        return instance
