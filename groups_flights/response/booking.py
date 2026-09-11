from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal

from groups_flights.models import GroupBookingDetail

from .flight import FlightResponse
from .serialize import to_json_dict


@dataclass
class GroupBookingDetailResponse:
    id: int
    group_id: int
    status: str
    adult_seats_requested: int
    child_seats_requested: int
    adult_price_per_seat: Decimal
    child_price_per_seat: Decimal
    total_amount: Decimal
    token_payment_deadline: datetime
    full_payment_deadline: datetime
    flight: FlightResponse

    @classmethod
    def from_model(cls, booking: GroupBookingDetail) -> "GroupBookingDetailResponse":
        return cls(
            id=booking.id,
            group_id=booking.group_id,
            status=booking.status,
            adult_seats_requested=booking.adult_seats_requested,
            child_seats_requested=booking.child_seats_requested,
            adult_price_per_seat=booking.adult_price_per_seat,
            child_price_per_seat=booking.child_price_per_seat,
            total_amount=booking.total_amount,
            token_payment_deadline=booking.token_payment_deadline,
            full_payment_deadline=booking.full_payment_deadline,
            flight=FlightResponse.from_model(booking.flight),
        )

    def to_dict(self) -> dict:
        data = to_json_dict(asdict(self))
        data["flight"] = self.flight.to_dict()
        return data
