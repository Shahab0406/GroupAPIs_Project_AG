from django.urls import path
from groups_flights.views import flight_info_api

urlpatterns = [
    # ... your existing URL patterns
    path("api/flight-info/", flight_info_api, name="flight_info_api"),
]