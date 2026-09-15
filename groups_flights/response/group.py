from dataclasses import asdict, dataclass

from groups_flights.models import Group
from groups_flights.utils import CurrencyConvert

from .flight import FlightResponse
from .serialize import to_json_dict


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
    selling_price_per_seat_child: CurrencyConvert | None
    token_amount: CurrencyConvert
    token_payment_deadline: int
    full_payment_deadline: int
    is_active: bool
    flights: list[FlightResponse]

    @classmethod
    def from_model(cls, group: Group) -> "GroupSummaryResponse":
        return cls(
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

    @classmethod
    def from_dict(cls, data: dict) -> "GroupSummaryResponse":
        selling_currency = data["selling_currency"]
        return cls(
            id=data["id"],
            group_name=data["group_name"],
            adult_seats=data["adult_seats"],
            available_adult_seats=data["available_adult_seats"],
            child_seats=data["child_seats"],
            available_child_seats=data["available_child_seats"],
            selling_currency=selling_currency,
            selling_price_per_seat_adult=CurrencyConvert.from_amount(
                data["selling_price_per_seat_adult"]["value"],
                selling_currency,
            ),
            selling_price_per_seat_child=(
                CurrencyConvert.from_amount(
                    data["selling_price_per_seat_child"]["value"],
                    selling_currency,
                )
                if data.get("selling_price_per_seat_child")
                else None
            ),
            token_amount=CurrencyConvert.from_amount(
                data["token_amount"]["value"],
                selling_currency,
            ),
            token_payment_deadline=int(data["token_payment_deadline"]),
            full_payment_deadline=int(data["full_payment_deadline"]),
            is_active=data["is_active"],
            flights=[FlightResponse.from_dict(flight) for flight in data.get("flights", [])],
        )

    def to_dict(self) -> dict:
        data = to_json_dict(asdict(self))
        data["flights"] = [flight.to_dict() for flight in self.flights]
        return data


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
    selling_price_per_seat_child: CurrencyConvert | None
    selling_price_per_seat_infant: CurrencyConvert
    is_active: bool
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

    def to_dict(self) -> dict:
        data = to_json_dict(asdict(self))
        data["flights"] = [flight.to_dict() for flight in self.flights]
        return data
