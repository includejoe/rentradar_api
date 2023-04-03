from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView

from base.utils.jwt_decoder import decode_jwt
from .models import User
from . import serializers

# Create your views here.
class UserDetailsAPIView(RetrieveUpdateAPIView):
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


class PublicUserDetailsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PublicUserSerializer

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise ParseError(detail=e, code=401)


public_user_details_view = PublicUserDetailsAPIView.as_view()
