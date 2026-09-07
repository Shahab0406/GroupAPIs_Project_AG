from dataclasses import asdict, dataclass
from datetime import datetime

from groups_flights.models import Flight

from .serialize import to_json_dict


@dataclass
class FlightResponse:
    id: int
    flight_number: str
    departure_datetime: datetime
    sector_from: str
    arrival_datetime: datetime
    sector_to: str
    travel_class: str
    baggage_allowance: str
    meal_available: bool

    @classmethod
    def from_model(cls, flight: Flight) -> "FlightResponse":
        return cls(
            id=flight.id,
            flight_number=flight.flight_number,
            departure_datetime=flight.departure_datetime,
            sector_from=flight.origin,
            arrival_datetime=flight.arrival_datetime,
            sector_to=flight.destination,
            travel_class=flight.travel_class,
            baggage_allowance=flight.baggage_allowance,
            meal_available=flight.meal_available,
        )

    def to_dict(self) -> dict:
        return to_json_dict(asdict(self))
