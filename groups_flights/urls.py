from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BookingView, GroupView, PaymentView, SegmentView

urlpatterns = [
    path("groups/", GroupView.list, name="group-list"),
    path("groups/<int:pk>/", GroupView.detail, name="group-detail"),
    path("bookings/", csrf_exempt(BookingView.create), name="create-booking"),
    path("bookings/<int:pk>/", BookingView.detail, name="booking-detail"),
    path("pay-now/", csrf_exempt(PaymentView.pay_now), name="pay-now"),
    path("flight-info/", SegmentView.flight_info, name="flight-info"),
]
