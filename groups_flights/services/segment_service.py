from groups_flights.models import Segment
from groups_flights.response import SegmentResponse


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
