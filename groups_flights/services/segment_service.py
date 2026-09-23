from groups_flights.models import Segment , Airline
from groups_flights.response import SegmentResponse
import re

from groups_flights.response.airline import AirlineData


class SegmentService:
    def map_segment_response(self, segment: Segment) -> dict:
        return SegmentResponse.from_model(segment).to_dict()

    def list_segments(self) -> list[dict]:
        segments = Segment.objects.all()
        return [self.map_segment_response(segment) for segment in segments]

    def get_segment(self, pk: int) -> dict | None:
        segment = Segment.objects.filter(pk=pk).first()
        if not segment:
            return None
        return self.map_segment_response(segment)

    def get_segment_by_flight_number(self, flight_number: str) -> dict | None:
        segment = Segment.objects.filter(flight_number=flight_number).first()
        if not segment:
            return None
        return SegmentResponse.from_model(segment).to_flight_info_dict()

    @staticmethod
    def normalize_flight_number(raw_str):
            clean_str = re.sub(r"[^A-Z0-9]", "", str(raw_str).upper())
            match = re.match(r"^([A-Z]+)(\d+)$", clean_str)
    
            if match:
                carrier_code, number = match.groups()
                return f"{carrier_code}-{number}", carrier_code
    
            carrier_code = "".join(filter(str.isalpha, clean_str))
            return clean_str, carrier_code

    def get_airline_info_by_carrier_code(self, carrier_code: str) -> dict | None:
        if not carrier_code:
            return None

        airline = Airline.objects.filter(code__iexact=carrier_code).first()

        if not airline:
            return None

        airline_data = AirlineData(
            airline_id=airline.id,
            airline_display=f"{airline.code} - {airline.name}",
        )
        
        return AirlineData(
            airline_id=airline.id,
            airline_display=f"{airline.code} - {airline.name}",
        )
        
    
    def get_flight_info_autofill(self, raw_flight_number: str) -> dict | None:
        formatted_number, carrier_code = self.normalize_flight_number(raw_flight_number)

        segment_data = self.get_segment_by_flight_number(formatted_number)
        airline_data = self.get_airline_info_by_carrier_code(carrier_code)
        if segment_data:
            if airline_data:
                segment_data.setdefault("airline", airline_data.airline_id)
                segment_data.setdefault(
                    "airline_display", airline_data.airline_display
                )
            return segment_data

        if airline_data:
            return airline_data.to_json()

        return None