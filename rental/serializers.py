from rest_framework import serializers
from django.utils import timezone

from .models import Rental
from user.serializers import UserInfoSerializer


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
