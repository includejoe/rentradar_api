from rest_framework import serializers

from .models import Property
from user.serializers import PublicUserSerializer


class PropertySerializer(serializers.ModelSerializer):
    # user = PublicUserSerializer(many=False)

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
