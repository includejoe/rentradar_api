from rest_framework import serializers

from .models import RentalReview, UserReview
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


class CreateRentalReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalReview
        fields = "__all__"

        read_only_fields = ["id", "created_at"]


class RentalReviewSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = RentalReview
        fields = "__all__"

        read_only_fields = ["id", "created_at"]
