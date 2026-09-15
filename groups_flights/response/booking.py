from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal

from groups_flights.models import GroupBookingDetail

from .group import GroupSummaryResponse
from .serialize import to_json_dict


@dataclass
class GroupBookingDetailResponse:
    id: int
    status: str
    adult_seats_requested: int
    child_seats_requested: int
    adult_price_per_seat: Decimal
    child_price_per_seat: Decimal
    total_amount: Decimal
    token_payment_deadline: datetime
    full_payment_deadline: datetime
    group: GroupSummaryResponse

    @classmethod
    def from_model(
        cls,
        booking: GroupBookingDetail,
        group: GroupSummaryResponse,
    ) -> "GroupBookingDetailResponse":
        return cls(
            id=booking.id,
            status=booking.status,
            adult_seats_requested=booking.adult_seats_requested,
            child_seats_requested=booking.child_seats_requested,
            adult_price_per_seat=booking.adult_price_per_seat,
            child_price_per_seat=booking.child_price_per_seat,
            total_amount=booking.total_amount,
            token_payment_deadline=booking.token_payment_deadline,
            full_payment_deadline=booking.full_payment_deadline,
            group=group,
        )

    def to_dict(self) -> dict:
        data = to_json_dict(asdict(self))
        data["group"] = self.group.to_dict()
        return data
