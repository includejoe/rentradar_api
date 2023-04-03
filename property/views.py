from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.generics import GenericAPIView

from . import serializers
from .models import Property

# Create your views here.
class PostPropertyAPIView(GenericAPIView):
    pass


post_property_view = PostPropertyAPIView.as_view()


class GetAllPropertiesAPIView(GenericAPIView):
    pass


get_all_properties_view = GetAllPropertiesAPIView.as_view()


class GetUserPropertiesAPIView(GenericAPIView):
    pass


get_user_properties_view = GetUserPropertiesAPIView.as_view()


class PropertyDetailAPIView(GenericAPIView):
    pass


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
            half_length = int(len(title) / 2)
            q = Q()
            for i in range(half_length, len(title) + 1):
                q |= Q(title__icontains=title[:i])
            properties = properties.filter(q)
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
