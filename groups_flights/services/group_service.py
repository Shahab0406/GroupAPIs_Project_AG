from groups_flights.models import Group
from groups_flights.response import GroupResponse


class GroupService:
    def _serialize_group(self, group: Group) -> dict:
        return GroupResponse.from_model(group).to_dict()

    def list_groups(self) -> list[dict]:
        groups = Group.objects.prefetch_related("flights").all()
        return [self._serialize_group(group) for group in groups]

    def get_group(self, pk: int) -> dict | None:
        group = Group.objects.prefetch_related("flights").filter(pk=pk).first()
        if not group:
            return None
        return self._serialize_group(group)
