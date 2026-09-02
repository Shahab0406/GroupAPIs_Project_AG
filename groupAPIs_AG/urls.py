from django.urls import path
from groupAPIs_AG.views import get_flight_info

urlpatterns = [
    # ... your existing URL patterns
    path('api/flight-info/', get_flight_info, name='get_flight_info'),
]