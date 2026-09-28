from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import config, dataclass_json

from groups_flights.models import Flight


def _encode_datetime(value: datetime) -> str:
    if value.tzinfo is not None:
        value = value.replace(tzinfo=None)
    return value.isoformat(timespec="seconds")


@dataclass_json
@dataclass
class FlightResponse:
    flight_number: str
    origin: str
    destination: str
    travel_class: str
    baggage_allowance: str
    meal_available: bool
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
    def from_model(cls, flight: Flight) -> "FlightResponse":
        return FlightResponse(
            flight_number=flight.flight_number,
            origin=flight.origin,
            destination=flight.destination,
            travel_class=flight.travel_class,
            baggage_allowance=flight.baggage_allowance,
            meal_available=flight.meal_available,
            departure_datetime=flight.departure_datetime,
            arrival_datetime=flight.arrival_datetime,
        )
