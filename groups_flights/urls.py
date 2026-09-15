from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BookingView, GroupView, flight_info_api

urlpatterns = [
    path("groups/", GroupView.list, name="group-list"),
    path("groups/<int:pk>/", GroupView.detail, name="group-detail"),
    path("bookings/", csrf_exempt(BookingView.create), name="create-booking"),
    path("flight-info/", flight_info_api, name="flight-info"),
]
