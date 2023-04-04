from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, APIException
from rest_framework.generics import GenericAPIView

from base.utils.jwt_decoder import decode_jwt
from . import serializers
from .models import Property
from user.models import User

# Create your views here.
class PostPropertyAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PropertySerializer

    def post(self, request):
        property_data = request.data
        token = request.headers["AUTHORIZATION"]
        user_id = decode_jwt(token)

        image1 = property_data.get("image1", None)
        image2 = property_data.get("image2", None)
        image3 = property_data.get("image3", None)
        image4 = property_data.get("image4", None)
        image5 = property_data.get("image5", None)

        if image1 is None or image1 == "":
            raise ParseError(detail="image1 can not be null or empty")

        if image2 is None or image2 == "":
            raise ParseError(detail="image2 can not be null or empty")

        if image3 is None or image3 == "":
            raise ParseError(detail="image3 can not be null or empty")

        if image4 is None or image4 == "":
            raise ParseError(detail="image4 can not be null or empty")

        if image5 is None or image5 == "":
            raise ParseError(detail="image5 can not be null or empty")

        try:
            user = User.objects.get(id=user_id)
            if user.user_type > 1:
                property_data["user"] = user
                new_property = Property(**property_data)
                new_property.save()
                serializer = self.serializer_class(new_property)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise ParseError(detail="A user of type 1 can not post a property")
        except Exception as e:
            raise APIException(detail=e)


post_property_view = PostPropertyAPIView.as_view()


class GetAllPropertiesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PropertySerializer

    def get(self, _):
        properties = Property.objects.all()
        serializer = self.serializer_class(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_all_properties_view = GetAllPropertiesAPIView.as_view()


class GetUserPropertiesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PropertySerializer

    def get(self, _, user_id):
        if User.objects.filter(id=user_id).exists() == False:
            raise ParseError(detail="This user does not exist", code=404)

        user = User.objects.get(id=user_id)
        properties = Property.objects.filter(user=user)
        serializer = self.serializer_class(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_user_properties_view = GetUserPropertiesAPIView.as_view()


class PropertyDetailAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PropertySerializer

    def get(self, _, property_id):
        if Property.objects.filter(id=property_id).exists() == False:
            raise ParseError(detail="This property does not exist", code=404)

        property = Property.objects.get(id=property_id)
        serializer = self.serializer_class(property)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, property_id):
        token = request.headers["AUTHORIZATION"]
        user_id = decode_jwt(token)
        property_owner = User.objects.get(id=user_id)

        if Property.objects.filter(id=property_id).exists() == False:
            raise ParseError(detail="This property does not exist", code=404)

        property_to_delete = Property.objects.get(id=property_id)

        if property_to_delete.user.id != property_owner.id:
            raise ParseError(detail="This user does not own this property", code=401)

        property_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, property_id):
        token = request.headers["AUTHORIZATION"]
        user_id = decode_jwt(token)
        property_data = request.data
        property_owner = User.objects.get(id=user_id)

        if Property.objects.filter(id=property_id).exists() == False:
            raise ParseError(detail="This property does not exist", code=404)

        property_to_update = Property.objects.get(id=property_id)

        if property_to_update.user.id != property_owner.id:
            raise ParseError(detail="This user does not own this property", code=401)

        serializer = self.serializer_class(
            property_to_update,
            data=property_data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


property_detail_view = PropertyDetailAPIView.as_view()


class FilterPropertiesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PropertySerializer

    def get(self, request):
        title = request.query_params.get("title", None)
        location = request.query_params.get("location", None)
        min_rate = request.query_params.get("min_rate", None)
        max_rate = request.query_params.get("max_rate", None)
        min_term = request.query_params.get("min_term", None)
        max_term = request.query_params.get("max_term", None)
        num_of_rooms = request.query_params.get("num_of_rooms", None)
        is_furnished = request.query_params.get("is_furnished", None)
        is_self_contain = request.query_params.get("is_self_contain", None)

        properties = Property.objects.all()
        if title:
            properties = properties.filter(title__icontains=title)
        if location:
            properties = properties.filter(location__icontains=location)
        if min_rate:
            properties = properties.filter(rate__gte=min_rate)
        if max_rate:
            properties = properties.filter(rate__lte=max_rate)
        if min_term:
            properties = properties.filter(lease_term_in_months__gte=min_term)
        if max_term:
            properties = properties.filter(lease_term_in_months__lte=max_term)
        if num_of_rooms:
            properties = properties.filter(num_of_rooms=num_of_rooms)
        if is_furnished is not None:
            properties = properties.filter(is_furnished=is_furnished)
        if is_self_contain is not None:
            properties = properties.filter(is_self_contain=is_self_contain)

        serializer = self.serializer_class(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


filter_properties_view = FilterPropertiesAPIView.as_view()
