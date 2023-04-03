from django.contrib.auth import authenticate
from rest_framework import serializers

from user.models import User
from base.utils.email_validator import is_email_valid


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "phone",
            "gender",
            "dob",
            "user_type",
        ]

    def validate_email(self, value):
        valid, error_message = is_email_valid(value)
        if not valid:
            raise serializers.ValidationError(error_message)

        try:
            email_name, domain = value.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            value = "@".join([email_name, domain.lower()])

        return value

    def validate(self, data):
        gender = data.get("gender", None)
        dob = data.get("dob", None)
        phone = data.get("phone", None)
        user_type = data.get("user_type", None)

        if gender is None:
            raise serializers.ValidationError("gender is required")

        if dob is None:
            raise serializers.ValidationError("dob is required")

        if phone is None:
            raise serializers.ValidationError("phone is required")

        if user_type is None:
            raise serializers.ValidationError("user_type is required")

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    jwt = serializers.SerializerMethodField()

    def get_jwt(self, obj):
        user = User.objects.get(email=obj.email)
        return user.tokens["access"]

    class Meta:
        model = User
        fields = ["email", "password", "jwt"]

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email is required")

        if password is None:
            raise serializers.ValidationError("A password is required")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError(
                "This user account is currently deactivated"
            )

        return user
