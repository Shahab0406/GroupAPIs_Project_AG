from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import config, dataclass_json

from groups_flights.models import Segment


def _encode_datetime(value: datetime) -> str:
    if value.tzinfo is not None:
        value = value.replace(tzinfo=None)
    return value.isoformat(timespec="seconds")


@dataclass_json
@dataclass
class SegmentResponse:
    id: int
    flight_number: str
    origin: str
    destination: str
    operating_airline: str
    marketing_airline: str
    departure_datetime: datetime = field(
        metadata=config(
            encoder=_encode_datetime,
            decoder=datetime.fromisoformat,
        ),
    )
    arrival_datetime: datetime = field(
        metadata=config(
            encoder=_encode_datetime,
            decoder=datetime.fromisoformat,
        ),
    )

    @classmethod
    def from_model(cls, segment: Segment) -> "SegmentResponse":
        return SegmentResponse(
            id=segment.id,
            flight_number=segment.flight_number,
            origin=segment.origin,
            destination=segment.destination,
            operating_airline=segment.operating_airline,
            marketing_airline=segment.marketing_airline,
            departure_datetime=segment.departure_datetime,
            arrival_datetime=segment.arrival_datetime,
        )

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
