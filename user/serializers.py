from django.contrib.auth import authenticate, login
from rest_framework import serializers
from django.utils import timezone

from .models import User, Rating, UserKyc
from base.utils import is_email_valid


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=128, write_only=True)
    last_name = serializers.CharField(max_length=128, write_only=True)
    bus_name = serializers.CharField(max_length=128, write_only=True, required=False)
    gender = serializers.CharField(max_length=12, write_only=True)
    phone = serializers.CharField(max_length=128, write_only=True)
    dob = serializers.CharField(max_length=32, write_only=True)
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    user_type = serializers.IntegerField(write_only=True)
    jwt = serializers.SerializerMethodField()

    def get_jwt(self, obj):
        user = User.objects.get(email=obj.email)
        return user.tokens["access"]

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "bus_name",
            "password",
            "phone",
            "gender",
            "dob",
            "user_type",
            "jwt",
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
        bus_name = data.get("bus_name", None)
        gender = data.get("gender", None)
        dob = data.get("dob", None)
        phone = data.get("phone", None)
        user_type = data.get("user_type", None)

        if user_type == 2 and bus_name is None:
            raise serializers.ValidationError(
                "bus_name can not be null for a user of type 2"
            )

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

    def validate(self, data):
        request = self.context.get("request")
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email is required")

        if password is None:
            raise serializers.ValidationError("A password is required")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if user.user_status == 2:
            raise serializers.ValidationError(
                "This user account is currently deactivated"
            )
        elif user.user_status == 3:
            raise serializers.ValidationError(
                "This user account is currently suspended"
            )
        elif user.user_status == 4:
            raise serializers.ValidationError("This user account has been deleted")

        login(request, user)
        return user

    class Meta:
        model = User
        fields = ["email", "password", "jwt"]


class UserInfoSerializer(serializers.ModelSerializer):
    is_kyc_verified = serializers.SerializerMethodField()

    def get_is_kyc_verified(self, obj):
        kyc = obj.kyc.first()
        if kyc:
            return kyc.verified
        else:
            return False

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "bus_name",
            "is_kyc_verified",
            "profile_image",
            "user_type",
        ]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    gender = serializers.SerializerMethodField()
    is_kyc_verified = serializers.SerializerMethodField()

    def get_is_kyc_verified(self, obj):
        kyc = obj.kyc.first()
        if kyc:
            return kyc.verified
        else:
            return False

    def get_gender(self, obj):
        return obj.get_gender_display()

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.updated_at = timezone.now
        instance.save()

        return instance

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
            "is_kyc_verified",
            "user_status",
            "last_login",
            "created_at",
        ]
        read_only_fields = ["id", "created_at" "full_name", "email", "last_login"]


class PublicUserSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    is_kyc_verified = serializers.SerializerMethodField()

    def get_is_kyc_verified(self, obj):
        kyc = obj.kyc.first()
        if kyc:
            return kyc.verified
        else:
            return False

    def get_gender(self, obj):
        return obj.get_gender_display()

    class Meta:
        model = User
        fields = [
            "full_name",
            "bus_name",
            "phone",
            "gender",
            "location",
            "is_kyc_verified",
            "rating",
            "created_at",
            "profile_image",
            "user_type",
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "user_rated", "rater", "value")
        read_only_fields = ("id", "user_rated", "rater")


class UserKycSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = UserKyc
        exclude = ["verified"]
