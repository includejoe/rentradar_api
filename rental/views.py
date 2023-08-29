from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ParseError, APIException
from rest_framework.generics import GenericAPIView

from . import serializers
from .models import Rental
from user.models import User


# Create your views here.
class CreateRentalAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateRentalSerializer

    def post(self, request):
        rental_data = request.data
        user = request.user

        try:
            if user.user_type > 1:
                rental_data["user"] = user
                new_rental = Rental(**rental_data)

                # perform validation
                new_rental.full_clean()

                new_rental.save()
                serializer = self.serializer_class(new_rental)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise ParseError(detail="A user of type 1 can not create a rental")
        except Exception as e:
            raise APIException(detail=e)


create_rental_view = CreateRentalAPIView.as_view()


class GetAllRentalsAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RentalSerializer

    def get(self, _):
        rentals = Rental.objects.all()
        serializer = self.serializer_class(rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_all_rentals_view = GetAllRentalsAPIView.as_view()


class GetUserRentalsAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RentalSerializer

    def get(self, _, user_id):
        if User.objects.filter(id=user_id).exists() == False:
            raise ParseError(detail="This user does not exist", code=404)

        user = User.objects.get(id=user_id)
        rentals = Rental.objects.filter(user=user)
        serializer = self.serializer_class(rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_user_rentals_view = GetUserRentalsAPIView.as_view()


class RentalDetailAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RentalSerializer

    def get(self, _, rental_id):
        if Rental.objects.filter(id=rental_id).exists() == False:
            raise ParseError(detail="This rental does not exist", code=404)

        rental = Rental.objects.get(id=rental_id)
        serializer = self.serializer_class(rental)
        return Response(serializer.data, status=status.HTTP_200_OK)


rental_detail_view = RentalDetailAPIView.as_view()


class UpdateRentalAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RentalSerializer

    def patch(self, request, rental_id):
        rental_owner = request.user
        rental_data = request.data

        if Rental.objects.filter(id=rental_id).exists() == False:
            raise ParseError(detail="This rental does not exist", code=404)

        rental_to_update = Rental.objects.get(id=rental_id)

        if rental_to_update.user.id != rental_owner.id:
            raise ParseError(detail="This user does not own this rental", code=401)

        serializer = self.serializer_class(
            rental_to_update,
            data=rental_data,
            partial=True,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


update_rental_view = UpdateRentalAPIView.as_view()


class DeleteRentalAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RentalSerializer

    def delete(self, request, rental_id):
        rental_owner = request.user

        if Rental.objects.filter(id=rental_id).exists() == False:
            raise ParseError(detail="This rental does not exist", code=404)

        rental_to_delete = Rental.objects.get(id=rental_id)

        if rental_to_delete.user.id != rental_owner.id:
            raise ParseError(detail="This user does not own this rental", code=401)

        rental_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


delete_rental_view = DeleteRentalAPIView.as_view()


class FilterRentalsAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RentalSerializer

    def get(self, request):
        title = request.query_params.get("title", None)
        location = request.query_params.get("location", None)
        category = request.query_params.get("category", None)
        min_rate = request.query_params.get("min_rate", None)
        max_rate = request.query_params.get("max_rate", None)
        min_term = request.query_params.get("min_term", None)
        max_term = request.query_params.get("max_term", None)

        rentals = Rental.objects.all()
        if title:
            rentals = rentals.filter(title__icontains=title)
        if location:
            rentals = rentals.filter(location__icontains=location)
        if category:
            rentals = rentals.filter(category__icontains=category)
        if min_rate:
            rentals = rentals.filter(rate__gte=min_rate)
        if max_rate:
            rentals = rentals.filter(rate__lte=max_rate)
        if min_term:
            rentals = rentals.filter(lease_term_in_months__gte=min_term)
        if max_term:
            rentals = rentals.filter(lease_term_in_months__lte=max_term)

        serializer = self.serializer_class(rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


filter_rentals_view = FilterRentalsAPIView.as_view()
