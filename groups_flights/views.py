from django.shortcuts import render
from django.http import JsonResponse
from groups_flights.models import Segment

# Create your views here.

def flight_info_api(request):
    flight_number = request.GET.get("flight_number", "").strip()

    if not flight_number:
        return JsonResponse(
            {"success": False, "error": "No flight number provided"}, status=400
        )

    # Search Segment for matching flight number
    segment = Segment.objects.filter(flight_number=flight_number).first()

    if not segment:
        return JsonResponse(
            {"success": False, "error": "Flight segment not found"}, status=404
        )

    # Split DateTime fields into Date (YYYY-MM-DD) and Time (HH:MM:SS) for admin widgets
    departure_date = (
        segment.departure_datetime.strftime("%Y-%m-%d")
        if segment.departure_datetime
        else ""
    )
    departure_time = (
        segment.departure_datetime.strftime("%H:%M:%S")
        if segment.departure_datetime
        else ""
    )
    arrival_date = (
        segment.arrival_datetime.strftime("%Y-%m-%d")
        if segment.arrival_datetime
        else ""
    )
    arrival_time = (
        segment.arrival_datetime.strftime("%H:%M:%S")
        if segment.arrival_datetime
        else ""
    )

    data = {
        "success": True,
        "origin": getattr(segment, "origin", getattr(segment, "sector_from", "")),
        "destination": getattr(
            segment, "destination", getattr(segment, "sector_to", "")
        ),
        "departure_date": departure_date,
        "departure_time": departure_time,
        "arrival_date": arrival_date,
        "arrival_time": arrival_time,
    }

    return JsonResponse(data)

# def get_flight_info(request):
#     flight_number = request.GET.get('flight_number')
#     if flight_number:
#         segment = Segment.objects.filter(flight_number=flight_number).first()
#         if segment:
#             return JsonResponse({
#                 'success': True,
#                 'origin': segment.origin,
#                 'destination': segment.destination,
#                 'operating_airline': segment.operating_airline,
#                 'marketing_airline': getattr(segment, 'marketing_airline', ''),
#                 'departure_date': segment.departure_datetime.strftime('%Y-%m-%d') if segment.departure_datetime else '',
#                 'departure_time': segment.departure_datetime.strftime('%H:%M:%S') if segment.departure_datetime else '',
#                 'arrival_date': segment.arrival_datetime.strftime('%Y-%m-%d') if segment.arrival_datetime else '',
#                 'arrival_time': segment.arrival_datetime.strftime('%H:%M:%S') if segment.arrival_datetime else '',
#             })
#     return JsonResponse({'success': False})