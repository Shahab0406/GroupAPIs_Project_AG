from dataclasses import dataclass

from dataclasses_json import dataclass_json

from groups_flights.models import Group
from groups_flights.utils import CurrencyConvert

from .flight import FlightResponse


@dataclass_json
@dataclass
class GroupSummaryResponse:
    id: int
    group_name: str
    adult_seats: int
    available_adult_seats: int
    child_seats: int
    available_child_seats: int
    selling_currency: str
    selling_price_per_seat_adult: CurrencyConvert
    token_amount: CurrencyConvert
    token_payment_deadline: int
    full_payment_deadline: int
    is_active: bool
    flights: list[FlightResponse]
    selling_price_per_seat_child: CurrencyConvert = None

    @classmethod
    def from_model(cls, group: Group) -> "GroupSummaryResponse":
        return GroupSummaryResponse(
            id=group.id,
            group_name=group.group_name,
            adult_seats=group.adult_seats,
            available_adult_seats=group.available_adult_seats,
            child_seats=group.child_seats,
            available_child_seats=group.available_child_seats,
            selling_currency=group.selling_currency,
            selling_price_per_seat_adult=CurrencyConvert.from_amount(
                group.selling_price_per_seat_adult,
                group.selling_currency,
            ),
            selling_price_per_seat_child=CurrencyConvert.from_amount_optional(
                group.selling_price_per_seat_child,
                group.selling_currency,
            ),
            token_amount=CurrencyConvert.from_amount(
                group.token_amount,
                group.selling_currency,
            ),
            token_payment_deadline=group.token_payment_deadline,
            full_payment_deadline=group.full_payment_deadline,
            is_active=group.is_active,
            flights=[FlightResponse.from_model(flight) for flight in group.flights.all()],
        )


@dataclass_json
@dataclass
class GroupResponse:
    id: int
    group_name: str
    adult_seats: int
    available_adult_seats: int
    child_seats: int
    available_child_seats: int
    token_payment_deadline: int
    full_payment_deadline: int
    token_amount: CurrencyConvert
    selling_currency: str
    selling_price_per_seat_adult: CurrencyConvert
    selling_price_per_seat_infant: CurrencyConvert
    is_active: bool
    flights: list[FlightResponse]
    selling_price_per_seat_child: CurrencyConvert = None

    @classmethod
    def from_model(cls, group: Group) -> "GroupResponse":
        return GroupResponse(
            id=group.id,
            group_name=group.group_name,
            adult_seats=group.adult_seats,
            available_adult_seats=group.available_adult_seats,
            child_seats=group.child_seats,
            available_child_seats=group.available_child_seats,
            token_payment_deadline=group.token_payment_deadline,
            full_payment_deadline=group.full_payment_deadline,
            token_amount=CurrencyConvert.from_amount(
                group.token_amount,
                group.selling_currency,
            ),
            selling_currency=group.selling_currency,
            selling_price_per_seat_adult=CurrencyConvert.from_amount(
                group.selling_price_per_seat_adult,
                group.selling_currency,
            ),
            selling_price_per_seat_child=CurrencyConvert.from_amount_optional(
                group.selling_price_per_seat_child,
                group.selling_currency,
            ),
            selling_price_per_seat_infant=CurrencyConvert.from_amount(
                group.selling_price_per_seat_infant,
                group.selling_currency,
            ),
            is_active=group.is_active,
            flights=[FlightResponse.from_model(flight) for flight in group.flights.all()],
        )
