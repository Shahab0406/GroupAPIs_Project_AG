from groups_flights.cache import GroupCache
from groups_flights.models import Group
from groups_flights.response import GroupResponse


class GroupService:
    def _cache_group(self, group: Group) -> dict:
        group_data = GroupResponse.from_model(group).to_dict()
        GroupCache.set(group.id, group_data)
        print(f"list_groups: group_id={group.id} saved to cache")
        return group_data

    def list_groups(self) -> list[dict]:
        group_ids = list(
            Group.objects.filter(is_active=True).values_list("id", flat=True)
        )

        cached_groups = {}
        missing_ids = []

        for group_id in group_ids:
            cached = GroupCache.get(group_id)
            if cached is not None:
                cached_groups[group_id] = cached
                print(f"list_groups: group_id={group_id} source=cache")
            else:
                missing_ids.append(group_id)

        if missing_ids:
            groups = Group.objects.prefetch_related("flights").filter(
                pk__in=missing_ids,
                is_active=True,
            )
            for group in groups:
                cached_groups[group.id] = self._cache_group(group)
                print(f"list_groups: group_id={group.id} source=database")

        print(
            f"list_groups: total={len(group_ids)} "
            f"from_cache={len(group_ids) - len(missing_ids)} "
            f"from_database={len(missing_ids)}"
        )

        return [cached_groups[group_id] for group_id in group_ids]

    def get_group(self, pk: int) -> dict | None:
        cached = GroupCache.get(pk)
        if cached is not None:
            return cached

        group = Group.objects.prefetch_related("flights").filter(pk=pk, is_active=True).first()
        if not group:
            return None

        return GroupResponse.from_model(group).to_dict()
