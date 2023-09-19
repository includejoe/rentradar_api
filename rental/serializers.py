from rest_framework import serializers
from django.utils import timezone

from .models import Rental
from user.serializers import UserInfoSerializer


class CreateRentalSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)

    class Meta:
        model = Rental
        fields = "__all__"

        read_only_fields = ["id", "created_at"]


class RentalSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.get_category_display()

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
