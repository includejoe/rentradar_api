from rest_framework import serializers

from .models import RentalReview, UserReview
from user.serializers import UserInfoSerializer


class CreateUserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = "__all__"

        read_only_fields = ["id", "created_at", "user"]


class UserReviewSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = UserReview
        fields = "__all__"

        read_only_fields = ["id", "created_at", "user", "user_reviewed", "body"]


class CreateRentalReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalReview
        fields = "__all__"

        read_only_fields = ["id", "created_at", "user"]


class RentalReviewSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = RentalReview
        fields = "__all__"

        read_only_fields = ["id", "created_at", "user", "rental_review", "body"]
