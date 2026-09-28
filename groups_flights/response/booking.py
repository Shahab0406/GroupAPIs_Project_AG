from dataclasses import dataclass

from dataclasses_json import dataclass_json

from groups_flights.models import GroupBookingDetail
from groups_flights.utils import CurrencyConvert

from .group import GroupSummaryResponse
from .invoice import GroupFlightsInvoiceResponse


@dataclass_json
@dataclass
class GroupBookingDetailResponse:
    id: int
    status: str
    adult_seats_requested: int
    child_seats_requested: int
    adult_price_per_seat: CurrencyConvert
    total_amount: CurrencyConvert
    group: GroupSummaryResponse
    invoices: list[GroupFlightsInvoiceResponse]
    child_price_per_seat: CurrencyConvert = None

    @classmethod
    def from_model(cls, booking: GroupBookingDetail) -> "GroupBookingDetailResponse":
        group = GroupSummaryResponse.from_model(booking.group)
        currency = group.selling_currency
        return GroupBookingDetailResponse(
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
            group=group,
            invoices=[
                GroupFlightsInvoiceResponse.from_model(invoice)
                for invoice in booking.invoices.all()
            ],
        )
