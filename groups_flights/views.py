from http import HTTPStatus

from django.http import JsonResponse

from .models import Segment
from .response import CoreResponse, CoreStatus
from .services import GroupService

group_service = GroupService()


def group_list(request):
    groups_data = group_service.list_groups()

    return CoreResponse.success_response(
        message="Groups retrieved successfully.",
        data={
            "count": len(groups_data),
            "results": groups_data,
        },
    )


def group_detail(request, pk):
    group_data = group_service.get_group(pk)

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


def flight_info_api(request):
    flight_number = request.GET.get("flight_number", "").strip()

    if not flight_number:
        return JsonResponse(
            {"success": False, "error": "No flight number provided"},
            status=400,
        )

    segment = Segment.objects.filter(flight_number=flight_number).first()

    if not segment:
        return JsonResponse(
            {"success": False, "error": "Flight segment not found"},
            status=404,
        )

    departure_date = (
        segment.departure_datetime.strftime("%Y-%m-%d")
        if segment.departure_datetime
        else ""
    )
    departure_time = (
        segment.departure_datetime.strftime("%H:%M:%S")
        if segment.departure_datetime
        else ""
    )
    arrival_date = (
        segment.arrival_datetime.strftime("%Y-%m-%d")
        if segment.arrival_datetime
        else ""
    )
    arrival_time = (
        segment.arrival_datetime.strftime("%H:%M:%S")
        if segment.arrival_datetime
        else ""
    )

    return JsonResponse(
        {
            "success": True,
            "origin": segment.origin,
            "destination": segment.destination,
            "departure_date": departure_date,
            "departure_time": departure_time,
            "arrival_date": arrival_date,
            "arrival_time": arrival_time,
        }
    )
