from http import HTTPStatus
from django.contrib.admin.views.decorators import staff_member_required
from .response import CoreResponse, CoreStatus
from .services import GroupService, SegmentService
from django.contrib.auth.decorators import login_required, user_passes_test

def is_superuser_and_staff(user):
    return user.is_authenticated and user.is_superuser and user.is_staff

group_service = GroupService()
segment_service = SegmentService()


def group_list(request):
    groups_data = group_service.list_groups()

    return CoreResponse.success_response(
        message="Groups retrieved successfully.",
        data={
            "count": len(groups_data),
            "groups": groups_data,
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

@login_required
@user_passes_test(is_superuser_and_staff)
def flight_info_api(request):
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

    segment_data = segment_service.get_segment_by_flight_number(flight_number)

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
