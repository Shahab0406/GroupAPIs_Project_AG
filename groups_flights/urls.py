from django.urls import path

from .views import flight_info_api, group_detail, group_list

urlpatterns = [
    path("groups/", group_list, name="group-list"),
    path("groups/<int:pk>/", group_detail, name="group-detail"),
    path("flight-info/", flight_info_api, name="flight-info"),
]
