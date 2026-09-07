from django.db import transaction

from groups_flights.exceptions import InsufficientSeatsError
from groups_flights.models import Flight, Group, GroupBookingDetail
from groups_flights.request.booking_request import BookingRequest
from groups_flights.response import GroupBookingDetailResponse
from groups_flights.utils import BookingStatus, TravelClass


class BookingService:
    def map_booking_response(self, booking: GroupBookingDetail) -> dict:
        return GroupBookingDetailResponse.from_model(booking).to_dict()

    def create_booking(self, group_id: int, booking_request: BookingRequest) -> dict:
        if booking_request.adult_seats_requested < 0 or booking_request.child_seats_requested < 0:
            raise ValueError("Requested seat counts cannot be negative.")

        if (
            booking_request.adult_seats_requested == 0
            and booking_request.child_seats_requested == 0
        ):
            raise ValueError("At least one adult or child seat must be requested.")

        if booking_request.travel_class not in TravelClass.values:
            raise ValueError(
                f"Invalid travel_class. Allowed values: {', '.join(TravelClass.values)}"
            )

        with transaction.atomic():
            group = Group.objects.select_for_update().filter(pk=group_id).first()
            if not group:
                return None

            if booking_request.adult_seats_requested > group.available_adult_seats:
                raise InsufficientSeatsError(
                    seat_type="adult",
                    requested=booking_request.adult_seats_requested,
                    available=group.available_adult_seats,
                )

            if booking_request.child_seats_requested > group.available_child_seats:
                raise InsufficientSeatsError(
                    seat_type="child",
                    requested=booking_request.child_seats_requested,
                    available=group.available_child_seats,
                )

            flight = Flight.objects.create(
                group=group,
                flight_number=booking_request.flight_number,
                departure_datetime=booking_request.departure_datetime,
                origin=booking_request.origin,
                arrival_datetime=booking_request.arrival_datetime,
                destination=booking_request.destination,
                travel_class=booking_request.travel_class,
                baggage_allowance=booking_request.baggage_allowance,
                meal_available=booking_request.meal_available,
            )

            booking = GroupBookingDetail.objects.create(
                group=group,
                flight=flight,
                status=BookingStatus.ON_HOLD,
                adult_seats_requested=booking_request.adult_seats_requested,
                child_seats_requested=booking_request.child_seats_requested,
                adult_price_per_seat=booking_request.adult_price_per_seat,
                child_price_per_seat=booking_request.child_price_per_seat,
                total_amount=booking_request.total_amount,
                token_payment_deadline=group.token_payment_deadline,
                full_payment_deadline=group.full_payment_deadline,
            )

            group.available_adult_seats -= booking_request.adult_seats_requested
            group.available_child_seats -= booking_request.child_seats_requested
            group.save(
                update_fields=["available_adult_seats", "available_child_seats"]
            )

        return self.map_booking_response(booking)
