from dataclasses import asdict, dataclass

from groups_flights.models import GroupBookingDetail
from groups_flights.utils import CurrencyConvert

from .group import GroupSummaryResponse
from .serialize import to_json_dict


@dataclass
class GroupBookingDetailResponse:
    id: int
    status: str
    adult_seats_requested: int
    child_seats_requested: int
    adult_price_per_seat: CurrencyConvert
    child_price_per_seat: CurrencyConvert | None
    total_amount: CurrencyConvert
    token_payment_deadline: int
    full_payment_deadline: int
    group: GroupSummaryResponse

    @classmethod
    def from_model(
        cls,
        booking: GroupBookingDetail,
        group: GroupSummaryResponse,
    ) -> "GroupBookingDetailResponse":
        currency = group.selling_currency
        return cls(
            id=booking.id,
            status=booking.status,
            adult_seats_requested=booking.adult_seats_requested,
            child_seats_requested=booking.child_seats_requested,
            adult_price_per_seat=CurrencyConvert.from_amount(
                booking.adult_price_per_seat,
                currency,
            ),
            child_price_per_seat=CurrencyConvert.from_amount_optional(
                booking.child_price_per_seat,
                currency,
            ),
            total_amount=CurrencyConvert.from_amount(booking.total_amount, currency),
            token_payment_deadline=booking.token_payment_deadline,
            full_payment_deadline=booking.full_payment_deadline,
            group=group,
        )

    def to_dict(self) -> dict:
        data = to_json_dict(asdict(self))
        data["group"] = self.group.to_dict()
        return data
