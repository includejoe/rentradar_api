from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, APIException
from rest_framework import generics

from base.utils.jwt_decoder import decode_jwt
from . import serializers
from .models import UserReview, RentalReview
from user.models import User
from rental.models import Rental


# Create your views here.
class CreateUserReviewAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateUserReviewSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        review_body = request.data.get("body")
        user_reviewed_id = request.data.get("user_reviewed")

        if user.id == user_reviewed_id:
            raise ParseError(
                detail="Users can not write reviews about themselves", code=401
            )

        try:
            user_reviewed = User.objects.get(id=user_reviewed_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "The user you are trying to review does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        review = UserReview(body=review_body, user_reviewed=user_reviewed, user=user)
        review.save()

        serializer = self.serializer_class(review)
        return Response(serializer.data, status=status.HTTP_200_OK)


create_user_review_view = CreateUserReviewAPIView.as_view()


class GetUserReviewsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserReviewSerializer

    def get(self, _, user_id):
        if User.objects.filter(id=user_id).exists() == False:
            raise ParseError(detail="This user does not exist", code=404)

        user_reviewed = User.objects.get(id=user_id)
        reviews = UserReview.objects.filter(user_reviewed=user_reviewed)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_user_reviews_view = GetUserReviewsAPIView.as_view()


class DeleteUserReviewAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserReviewSerializer

    def delete(self, request, review_id):
        review_owner = request.user

        if not UserReview.objects.filter(id=review_id).exists():
            raise ParseError(detail="This user review does not exist", code=404)

        review_to_delete = UserReview.objects.get(id=review_id)

        if review_to_delete.user != review_owner:
            raise ParseError(detail="This user does not own this review", code=401)

        review_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


delete_user_review_view = DeleteUserReviewAPIView.as_view()


class CreateRentalReviewAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateRentalReviewSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        review_body = request.data.get("body")
        rental_reviewed_id = request.data.get("rental_reviewed")

        try:
            rental_reviewed = Rental.objects.get(id=rental_reviewed_id)
        except Rental.DoesNotExist:
            return Response(
                {"detail": "The rental you are trying to review does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        review = RentalReview(
            body=review_body, rental_reviewed=rental_reviewed, user=user
        )
        review.save()

        serializer = self.serializer_class(review)
        return Response(serializer.data, status=status.HTTP_200_OK)


create_rental_review_view = CreateRentalReviewAPIView.as_view()


class GetRentalReviewsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RentalReviewSerializer

    def get(self, _, rental_id):
        print(rental_id)
        if Rental.objects.filter(id=rental_id).exists() == False:
            raise ParseError(detail="This rental does not exist", code=404)

        rental_reviewed = Rental.objects.get(id=rental_id)
        reviews = RentalReview.objects.filter(rental_reviewed=rental_reviewed)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_rental_reviews_view = GetRentalReviewsAPIView.as_view()


class DeleteRentalReviewAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RentalReviewSerializer

    def delete(self, request, review_id):
        review_owner = request.user

        if not RentalReview.objects.filter(id=review_id).exists():
            raise ParseError(detail="This rental review does not exist", code=404)

        review_to_delete = RentalReview.objects.get(id=review_id)

        if review_to_delete.user != review_owner:
            raise ParseError(detail="This user does not own this review", code=401)

        review_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


delete_rental_review_view = DeleteRentalReviewAPIView.as_view()
