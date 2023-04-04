from rest_framework import serializers

from .models import PropertyReview, UserReview
from user.serializers import UserInfoSerializer


class CreateUserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = "__all__"

        read_only_fields = ["id", "created_at"]


class UserReviewSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = UserReview
        fields = "__all__"

        read_only_fields = ["id", "created_at"]


class CreatePropertyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyReview
        fields = "__all__"

        read_only_fields = ["id", "created_at"]


class PropertyReviewSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = PropertyReview
        fields = "__all__"

        read_only_fields = ["id", "created_at"]
