from http import HTTPStatus

from groups_flights.models import Group
from groups_flights.response import CoreResponse, CoreStatus, GroupResponse


class GroupService:
    def _serialize_group(self, group: Group) -> dict:
        return GroupResponse.from_model(group).to_dict()

    def list_groups(self):
        groups = Group.objects.prefetch_related("flights").all()
        groups_data = [self._serialize_group(group) for group in groups]

        return CoreResponse.success_response(
            message="Groups retrieved successfully.",
            data={
                "count": len(groups_data),
                "results": groups_data,
            },
        )

    def get_group(self, pk: int):
        try:
            group = Group.objects.prefetch_related("flights").get(pk=pk)
        except Group.DoesNotExist:
            response = CoreResponse.generate_response(
                success=False,
                message="Group not found.",
                status=CoreStatus.Error.value,
                data={},
                error={"detail": f"No group exists with id {pk}."},
            )
            return CoreResponse.send_error_response(
                response,
                status=HTTPStatus.NOT_FOUND,
            )

        return CoreResponse.success_response(
            message="Group retrieved successfully.",
            data=self._serialize_group(group),
        )
