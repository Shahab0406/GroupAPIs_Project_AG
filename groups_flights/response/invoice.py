from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import config, dataclass_json

from groups_flights.models import GroupFlightsInvoice


def _encode_datetime(value: datetime) -> str:
    if value.tzinfo is not None:
        value = value.replace(tzinfo=None)
    return value.isoformat(timespec="seconds")


@dataclass_json
@dataclass
class GroupFlightsInvoiceResponse:
    id: int
    invoice_number: str | None
    invoice_status: str
    payment_status: str
    financial_profile: str | None
    payment_deadline: datetime | None = field(
        default=None,
        metadata=config(
            encoder=lambda value: _encode_datetime(value) if value else None,
            decoder=datetime.fromisoformat,
        ),
    )

    @classmethod
    def from_model(cls, invoice: GroupFlightsInvoice) -> "GroupFlightsInvoiceResponse":
        return cls(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            invoice_status=invoice.invoice_status,
            payment_status=invoice.payment_status,
            financial_profile=invoice.financial_profile,
            payment_deadline=invoice.payment_deadline,
        )


@dataclass_json
@dataclass
class InvoiceGroupContextResponse:
    id: int
    invoice_number: str | None
    group_name: str | None


@dataclass_json
@dataclass
class InvoiceBookingContextResponse:
    id: int
    group_name: str | None
    status: str


@dataclass_json
@dataclass
class GroupInvoiceDetailResponse:
    group_invoice: GroupFlightsInvoiceResponse
    group: InvoiceGroupContextResponse | None
    booking_details: InvoiceBookingContextResponse | None

    @classmethod
    def from_model(cls, invoice: GroupFlightsInvoice) -> "GroupInvoiceDetailResponse":
        group = getattr(invoice.booking_details, "group", None)
        return cls(
            group_invoice=GroupFlightsInvoiceResponse.from_model(invoice),
            group=(
                InvoiceGroupContextResponse(
                    id=group.id,
                    invoice_number=invoice.invoice_number,
                    group_name=group.group_name,
                )
                if group
                else None
            ),
            booking_details=(
                InvoiceBookingContextResponse(
                    id=invoice.booking_details.id,
                    group_name=group.group_name if group else None,
                    status=invoice.booking_details.status,
                )
                if invoice.booking_details
                else None
            ),
        )
