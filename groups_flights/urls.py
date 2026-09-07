from django.urls import path

from .views import BookingView, GroupView, SegmentView

urlpatterns = [
    path("groups/", GroupView.list, name="group-list"),
    path("groups/<int:pk>/", GroupView.detail, name="group-detail"),
    path("groups/<int:pk>/booking/", BookingView.create, name="create-booking"),
    path("flight-info/", SegmentView.flight_info, name="flight-info"),
]
