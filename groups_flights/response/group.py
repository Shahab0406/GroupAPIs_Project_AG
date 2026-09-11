from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal

from groups_flights.models import Group

from .flight import FlightResponse
from .serialize import to_json_dict


@dataclass
class GroupResponse:
    id: int
    group_name: str
    adult_seats: int
    available_adult_seats: int
    child_seats: int
    available_child_seats: int
    token_payment_deadline: datetime
    full_payment_deadline: datetime
    token_amount: Decimal
    buying_currency: str
    buying_price_per_seat_adult: Decimal
    buying_price_per_seat_child: Decimal
    buying_price_per_seat_infant: Decimal
    selling_currency: str
    selling_price_per_seat_adult: Decimal
    selling_price_per_seat_child: Decimal
    selling_price_per_seat_infant: Decimal
    pnr: str
    is_active: bool
    is_published: bool
    flights: list[FlightResponse]

    @classmethod
    def from_model(cls, group: Group) -> "GroupResponse":
        return cls(
            id=group.id,
            group_name=group.group_name,
            adult_seats=group.adult_seats,
            available_adult_seats=group.available_adult_seats,
            child_seats=group.child_seats,
            available_child_seats=group.available_child_seats,
            token_payment_deadline=group.token_payment_deadline,
            full_payment_deadline=group.full_payment_deadline,
            token_amount=group.token_amount,
            buying_currency=group.buying_currency,
            buying_price_per_seat_adult=group.buying_price_per_seat_adult,
            buying_price_per_seat_child=group.buying_price_per_seat_child,
            buying_price_per_seat_infant=group.buying_price_per_seat_infant,
            selling_currency=group.selling_currency,
            selling_price_per_seat_adult=group.selling_price_per_seat_adult,
            selling_price_per_seat_child=group.selling_price_per_seat_child,
            selling_price_per_seat_infant=group.selling_price_per_seat_infant,
            pnr=group.pnr,
            is_active=group.is_active,
            is_published=group.is_published,
            flights=[FlightResponse.from_model(flight) for flight in group.flights.all()],
        )

    def to_dict(self) -> dict:
        return to_json_dict(asdict(self))
