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
    invoice_status: str
    payment_status: str
    invoice_number: str = None
    financial_profile: str = None
    payment_deadline: datetime = field(
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
class PayNowResponse:
    invoice: GroupFlightsInvoiceResponse

    @classmethod
    def from_model(cls, invoice: GroupFlightsInvoice) -> "PayNowResponse":
        return cls(
            invoice=GroupFlightsInvoiceResponse.from_model(invoice),
        )

