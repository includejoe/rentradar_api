from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ParseError, APIException
from rest_framework.generics import GenericAPIView

from . import serializers
from .models import Rental
from user.models import User
from base.utils import action_response


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


class GetAllRentalsAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RentalSerializer

    def get(self, request):
        rentals = Rental.objects.all()
        serializer = self.serializer_class(
            rentals,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserRentalsAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RentalSerializer

    def get(self, request, user_id):
        if User.objects.filter(id=user_id).exists() == False:
            raise ParseError(detail="This user does not exist", code=404)

        user = User.objects.get(id=user_id)
        rentals = Rental.objects.filter(user=user)
        serializer = self.serializer_class(
            rentals,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class RentalDetailAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RentalSerializer

    def get(self, request, rental_id):
        if Rental.objects.filter(id=rental_id).exists() == False:
            raise ParseError(detail="This rental does not exist", code=404)

        rental = Rental.objects.get(id=rental_id)
        serializer = self.serializer_class(rental, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        return Response(
            action_response(success=True, info="Rental deleted successfully"),
            status=status.HTTP_204_NO_CONTENT,
        )


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

        # if no query params are provided, return empty list
        if (
            title is None
            and location is None
            and category is None
            and min_rate is None
            and max_rate is None
            and min_term is None
            and max_term is None
        ):
            rentals = Rental.objects.filter(pk__in=[])
        else:
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

        serializer = self.serializer_class(
            rentals,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFavoritesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RentalSerializer

    def get(self, request):
        user = request.user
        rentals = user.favorites.all()
        serializer = self.serializer_class(
            rentals,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        rental_id = request.data.get("rental_id", None)

        if rental_id is None:
            raise ParseError(detail="rental_id is required", code=400)

        if Rental.objects.filter(id=rental_id).exists() == False:
            raise ParseError(detail="This rental does not exist", code=404)

        rental = Rental.objects.get(id=rental_id)

        if user.favorites.filter(id=rental_id).exists():
            user.favorites.remove(rental)
            info = "This rental has been removed from favorites successfully"
        else:
            user.favorites.add(rental)
            info = "This rental has been added to favorites successfully"

        user.save()
        return Response(
            action_response(
                success=True,
                info=info,
            ),
            status=status.HTTP_200_OK,
        )


create_rental_view = CreateRentalAPIView.as_view()
get_all_rentals_view = GetAllRentalsAPIView.as_view()
get_user_rentals_view = GetUserRentalsAPIView.as_view()
rental_detail_view = RentalDetailAPIView.as_view()
update_rental_view = UpdateRentalAPIView.as_view()
delete_rental_view = DeleteRentalAPIView.as_view()
filter_rentals_view = FilterRentalsAPIView.as_view()
user_favorites_view = UserFavoritesAPIView.as_view()
