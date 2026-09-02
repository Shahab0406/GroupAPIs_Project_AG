from django.shortcuts import render
from django.http import JsonResponse
from groupAPIs_AG.models import Segments

def get_flight_info(request):
    flight_number = request.GET.get('flight_number')
    if flight_number:
        segment = Segments.objects.filter(flight_number=flight_number).first()
        if segment:
            return JsonResponse({
                'success': True,
                'origin': segment.origin,
                'destination': segment.destination,
                'operating_airline': segment.operating_airline,
                'marketing_airline': getattr(segment, 'marketing_airline', ''),
                'departure_date': segment.departure_datetime.strftime('%Y-%m-%d') if segment.departure_datetime else '',
                'departure_time': segment.departure_datetime.strftime('%H:%M:%S') if segment.departure_datetime else '',
                'arrival_date': segment.arrival_datetime.strftime('%Y-%m-%d') if segment.arrival_datetime else '',
                'arrival_time': segment.arrival_datetime.strftime('%H:%M:%S') if segment.arrival_datetime else '',
            })
    return JsonResponse({'success': False})