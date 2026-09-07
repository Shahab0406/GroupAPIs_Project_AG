from dataclasses import asdict, dataclass
from datetime import datetime

from groups_flights.models import Segment

from .serialize import to_json_dict


@dataclass
class SegmentResponse:
    id: int
    flight_number: str
    departure_datetime: datetime
    arrival_datetime: datetime
    origin: str
    destination: str
    operating_airline: str
    marketing_airline: str

    @classmethod
    def from_model(cls, segment: Segment) -> "SegmentResponse":
        return cls(
            id=segment.id,
            flight_number=segment.flight_number,
            departure_datetime=segment.departure_datetime,
            arrival_datetime=segment.arrival_datetime,
            origin=segment.origin,
            destination=segment.destination,
            operating_airline=segment.operating_airline,
            marketing_airline=segment.marketing_airline,
        )

    def to_dict(self) -> dict:
        return to_json_dict(asdict(self))

    def to_flight_info_dict(self) -> dict:
        data = self.to_dict()
        data.update(
            {
                "departure_date": (
                    self.departure_datetime.strftime("%Y-%m-%d")
                    if self.departure_datetime
                    else ""
                ),
                "departure_time": (
                    self.departure_datetime.strftime("%H:%M:%S")
                    if self.departure_datetime
                    else ""
                ),
                "arrival_date": (
                    self.arrival_datetime.strftime("%Y-%m-%d")
                    if self.arrival_datetime
                    else ""
                ),
                "arrival_time": (
                    self.arrival_datetime.strftime("%H:%M:%S")
                    if self.arrival_datetime
                    else ""
                ),
            }
        )
        return data
