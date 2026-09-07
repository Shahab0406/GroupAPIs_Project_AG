from http import HTTPStatus

from .exceptions import InsufficientSeatsError
from .request.booking_request import BookingRequest
from .response import CoreResponse, CoreStatus
from .services import BookingService, GroupService, SegmentService


class GroupView:
    service = GroupService()

    @staticmethod
    def list(request):
        groups_data = GroupView.service.list_groups()

        return CoreResponse.success_response(
            message="Groups retrieved successfully.",
            data={
                "count": len(groups_data),
                "groups": groups_data,
            },
        )

    @staticmethod
    def detail(request, pk):
        group_data = GroupView.service.get_group(pk)

        if group_data is None:
            response = CoreResponse.generate_response(
                success=False,
                message="Group not found.",
                status=CoreStatus.Error.value,
                data={},
                error={"detail": f"No group exists with id {pk}."},
            )
            return CoreResponse.send_error_response(response, status=HTTPStatus.NOT_FOUND)

        return CoreResponse.success_response(
            message="Group retrieved successfully.",
            data=group_data,
        )


class SegmentView:
    service = SegmentService()

    @staticmethod
    def flight_info(request):
        flight_number = request.GET.get("flight_number", "").strip()

        if not flight_number:
            response = CoreResponse.generate_response(
                success=False,
                message="No flight number provided.",
                status=CoreStatus.Error.value,
                data={},
                error={"detail": "flight_number query parameter is required."},
            )
            return CoreResponse.send_error_response(response, status=HTTPStatus.BAD_REQUEST)

        segment_data = SegmentView.service.get_segment_by_flight_number(flight_number)

        if segment_data is None:
            response = CoreResponse.generate_response(
                success=False,
                message="Flight segment not found.",
                status=CoreStatus.Error.value,
                data={},
                error={"detail": f"No segment exists with flight number {flight_number}."},
            )
            return CoreResponse.send_error_response(response, status=HTTPStatus.NOT_FOUND)

        return CoreResponse.success_response(
            message="Flight segment retrieved successfully.",
            data=segment_data,
        )


class BookingView:
    service = BookingService()

    @staticmethod
    def create(request, pk):
        try:
            booking_request = BookingRequest.from_json(request.body)
        except ValueError as exc:
            response = CoreResponse.generate_response(
                success=False,
                message="Invalid booking request.",
                status=CoreStatus.Error.value,
                data={},
                error={"detail": str(exc)},
            )
            return CoreResponse.send_error_response(response, status=HTTPStatus.BAD_REQUEST)

        try:
            booking_data = BookingView.service.create_booking(pk, booking_request)
        except InsufficientSeatsError as exc:
            response = CoreResponse.generate_response(
                success=False,
                message="Insufficient seats available.",
                status=CoreStatus.Error.value,
                data={},
                error={
                    "detail": str(exc),
                    "seat_type": exc.seat_type,
                    "requested": exc.requested,
                    "available": exc.available,
                },
            )
            return CoreResponse.send_error_response(response, status=HTTPStatus.BAD_REQUEST)
        except ValueError as exc:
            response = CoreResponse.generate_response(
                success=False,
                message="Invalid booking request.",
                status=CoreStatus.Error.value,
                data={},
                error={"detail": str(exc)},
            )
            return CoreResponse.send_error_response(response, status=HTTPStatus.BAD_REQUEST)

        if booking_data is None:
            response = CoreResponse.generate_response(
                success=False,
                message="Group not found.",
                status=CoreStatus.Error.value,
                data={},
                error={"detail": f"No group exists with id {pk}."},
            )
            return CoreResponse.send_error_response(response, status=HTTPStatus.NOT_FOUND)

        response = CoreResponse.generate_response(
            success=True,
            message="Booking created successfully.",
            status=CoreStatus.Success.value,
            data=booking_data,
            error={},
        )
        return CoreResponse.send_response(response, http_status=HTTPStatus.CREATED)
