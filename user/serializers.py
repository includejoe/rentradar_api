from rest_framework import serializers

from .models import User


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
            "password",
            "phone",
            "gender",
            "dob",
            "id_card_image",
            "profile_image",
            "user_type",
            "agent_fee",
            "agent_rating",
            "is_verified",
            "is_active",
            "created_at",
        ]

        read_only_fields = ["id", "created_at" "full_name", "email"]

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
