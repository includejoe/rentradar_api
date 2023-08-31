from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ParseError
from rest_framework import generics

from .models import User, Rating
from . import serializers


# Create your views here.
class RegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


register_user_view = RegistrationAPIView.as_view()


class LoginAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


login_user_view = LoginAPIView.as_view()


class UserDetailsAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # Return user on get request
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # Return updated user
        user = request.data
        serializer = self.serializer_class(
            request.user,
            data=user,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


user_details_view = UserDetailsAPIView.as_view()


class PublicUserDetailsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PublicUserSerializer

    def get(self, _, user_id):
        if User.objects.filter(id=user_id).exists() == False:
            raise ParseError(detail="This user does not exist", code=404)
        user = User.objects.get(id=user_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


public_user_details_view = PublicUserDetailsAPIView.as_view()


class RateUserAPIView(generics.CreateAPIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, user_id):
        rater = request.user
        value = request.data.get("value")

        if not value or not (1 <= value <= 5):
            return Response(
                {"detail": "Invalid rating value. Rating value must range from 1 to 5"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_rated = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "The user you are trying to rate does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user_rated == rater:
            return Response(
                {"detail": "Users can not rate themselves"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rating, created = Rating.objects.get_or_create(
            rater=rater, user_rated=user_rated, defaults={"value": value}
        )

        if not created:
            rating.value = value
            rating.save()

        serializer = self.serializer_class(rating)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


rate_user_view = RateUserAPIView.as_view()
