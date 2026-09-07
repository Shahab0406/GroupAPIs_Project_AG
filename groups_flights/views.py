from .services import GroupService

group_service = GroupService()


def group_list(request):
    return group_service.list_groups()


def group_detail(request, pk):
    return group_service.get_group(pk)
