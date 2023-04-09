from rest_framework import serializers
from django.utils import timezone

from .models import Rental
from user.serializers import UserInfoSerializer


class CreateRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = [
            "title",
            "description",
            "category",
            "location",
            "rate",
            "lease_term",
            "lease_cost",
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
        ]


class RentalSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = Rental
        fields = "__all__"

        read_only_fields = ["id", "user", "created_at"]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.updated_at = timezone.now
        instance.save()

        return instance
