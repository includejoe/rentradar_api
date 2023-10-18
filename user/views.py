from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ParseError, APIException
from rest_framework import generics

from .models import User, Rating, UserKyc
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


class LoginAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(
            data=user,
            context={"request": request},
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailsAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def retrieve(self, request):
        # Return user on get request
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
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


class PublicUserDetailsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PublicUserSerializer

    def get(self, _, email):
        if User.objects.filter(email=email).exists() == False:
            raise ParseError(detail="This user does not exist", code=404)
        user = User.objects.get(email=email)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RateUserAPIView(generics.CreateAPIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, email):
        rater = request.user
        value = request.data.get("value")

        if not value or not (1 <= value <= 5):
            return Response(
                {"detail": "Invalid rating value. Rating value must range from 1 to 5"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_rated = User.objects.get(email=email)
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


class UserKycAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserKycSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        data["user"] = request.user
        try:
            kyc = UserKyc.objects.create(**data)
            serializer = self.serializer_class(kyc)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise APIException(detail=str(e))


class KycStatusAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.UserKycSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        try:
            kyc = UserKyc.objects.get(user=request.user)
            serializer = self.serializer_class(kyc)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserKyc.DoesNotExist:
            return Response({"verified": False}, status=status.HTTP_200_OK)


register_user_view = RegistrationAPIView.as_view()
login_user_view = LoginAPIView.as_view()
user_details_view = UserDetailsAPIView.as_view()
public_user_details_view = PublicUserDetailsAPIView.as_view()
rate_user_view = RateUserAPIView.as_view()
user_kyc_view = UserKycAPIView.as_view()
kyc_status_view = KycStatusAPIView.as_view()
