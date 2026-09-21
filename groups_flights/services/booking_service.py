from decimal import Decimal

from django.db import transaction

from groups_flights.cache import GroupCache
from groups_flights.exceptions import InsufficientSeatsError
from groups_flights.models import Group, GroupBookingDetail, GroupFlightsInvoice
from groups_flights.request.booking_request import BookingRequest
from groups_flights.response import GroupBookingDetailResponse
from groups_flights.utils import BookingStatus


class BookingService:
    @staticmethod
    def _create_booking_invoices(booking: GroupBookingDetail, group: Group) -> None:
        GroupFlightsInvoice.objects.create(
            booking_details=booking,
            payment_deadline=group.get_token_payment_deadline(),
        )
        GroupFlightsInvoice.objects.create(
            booking_details=booking,
            payment_deadline=group.get_full_payment_deadline(),
        )

    def create_booking(self, booking_request: BookingRequest) -> dict:
        if booking_request.adult_seats_requested < 0 or booking_request.child_seats_requested < 0:
            raise ValueError("Requested seat counts cannot be negative.")

        if (
            booking_request.adult_seats_requested == 0
            and booking_request.child_seats_requested == 0
        ):
            raise ValueError("At least one adult or child seat must be requested.")

        with transaction.atomic():
            group = (
                Group.objects.select_for_update()
                .prefetch_related("flights")
                .filter(pk=booking_request.group_id, is_active=True)
                .first()
            )
            if not group:
                return None

            if (
                booking_request.adult_seats_requested > 0
                and group.selling_price_per_seat_adult <= 0
            ):
                raise ValueError(
                    "Adult seats cannot be booked when the adult selling price is zero."
                )

            if (
                booking_request.child_seats_requested > 0
                and group.selling_price_per_seat_child <= 0
            ):
                raise ValueError(
                    "Child seats cannot be booked when the child selling price is zero."
                )

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

            adult_price_per_seat = group.selling_price_per_seat_adult
            child_price_per_seat = group.selling_price_per_seat_child
            total_amount = (
                Decimal(booking_request.adult_seats_requested) * adult_price_per_seat
                + Decimal(booking_request.child_seats_requested) * child_price_per_seat
            )

            booking = GroupBookingDetail.objects.create(
                group=group,
                status=BookingStatus.ON_HOLD,
                adult_seats_requested=booking_request.adult_seats_requested,
                child_seats_requested=booking_request.child_seats_requested,
                adult_price_per_seat=adult_price_per_seat,
                child_price_per_seat=child_price_per_seat,
                total_amount=total_amount,
            )

            self._create_booking_invoices(booking, group)

            group.available_adult_seats -= booking_request.adult_seats_requested
            group.available_child_seats -= booking_request.child_seats_requested
            group.save(
                update_fields=["available_adult_seats", "available_child_seats"]
            )
            GroupCache.delete(booking_request.group_id)

        booking = (
            GroupBookingDetail.objects.select_related("group")
            .prefetch_related("group__flights", "invoices")
            .get(pk=booking.pk)
        )
        return self._serialize_booking(booking)

    @staticmethod
    def _serialize_booking(booking: GroupBookingDetail) -> dict:
        return GroupBookingDetailResponse.from_model(booking).to_dict()

    def get_booking_detail(self, booking_id: int) -> dict | None:
        booking = (
            GroupBookingDetail.objects.select_related("group")
            .prefetch_related("group__flights", "invoices")
            .filter(pk=booking_id)
            .first()
        )
        if not booking:
            return None

        return self._serialize_booking(booking)
