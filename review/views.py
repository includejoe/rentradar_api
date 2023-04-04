from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, APIException
from rest_framework.generics import GenericAPIView

from base.utils.jwt_decoder import decode_jwt
from . import serializers
from .models import UserReview, PropertyReview
from user.models import User
from property.models import Property

# Create your views here.
class CreateUserReviewAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateUserReviewSerializer

    def post(self, request):
        token = request.headers["AUTHORIZATION"]
        user_id = decode_jwt(token)
        review_data = {**request.data, "user": user_id}

        if user_id == review_data["user_reviewed"]:
            raise ParseError(
                detail="Users can not write reviews about themselves", code=401
            )

        serializer = self.serializer_class(data=review_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


create_user_review_view = CreateUserReviewAPIView.as_view()


class GetUserReviewsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserReviewSerializer

    def get(self, request, user_id):
        pass


get_user_reviews_view = GetUserReviewsAPIView.as_view()


class DeleteUserReviewAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserReviewSerializer

    def delete(self, request, review_id):
        pass


delete_user_review_view = DeleteUserReviewAPIView.as_view()


class CreatePropertyReviewAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreatePropertyReviewSerializer

    def post(self, request):
        token = request.headers["AUTHORIZATION"]
        user_id = decode_jwt(token)
        review_data = {**request.data, "user": user_id}

        serializer = self.serializer_class(data=review_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


create_property_review_view = CreatePropertyReviewAPIView.as_view()


class GetPropertyReviewsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PropertyReviewSerializer

    def get(self, request, property_id):
        pass


get_property_reviews_view = GetPropertyReviewsAPIView.as_view()


class DeletePropertyReviewAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PropertyReviewSerializer

    def delete(self, request, review_id):
        pass


delete_property_review_view = DeletePropertyReviewAPIView.as_view()
