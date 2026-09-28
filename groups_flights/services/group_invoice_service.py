from decimal import Decimal

from django.db import transaction

from groups_flights.models import GroupBookingDetail, GroupFlightsInvoice
from groups_flights.response.invoice import PayNowResponse
from groups_flights.utils import BookingStatus
from groups_flights.utils.status import PaymentStatus


class GroupInvoiceService:
    # Temporary in-memory balance until wallet integration is added.
    available_balance = Decimal("1400.00")

    @staticmethod
    def _get_next_unpaid_invoice(
        booking: GroupBookingDetail,
    ) -> GroupFlightsInvoice | None:
        return booking.invoices.filter(payment_status=PaymentStatus.UNPAID).first()

    @staticmethod
    def _get_payment_amount(booking: GroupBookingDetail) -> Decimal:
        paid_invoices = booking.invoices.filter(
            payment_status=PaymentStatus.PAID,
        ).count()
        if paid_invoices == 0:
            return booking.group.token_amount
        return booking.total_amount - booking.group.token_amount

    def pay_now(self, booking_id: int) -> dict | None:
        booking = (
            GroupBookingDetail.objects.select_related("group")
            .filter(pk=booking_id)
            .first()
        )
        if not booking:
            return None

        if booking.status != BookingStatus.ON_HOLD:
            raise ValueError("Booking is not active for payment.")

        invoice = self._get_next_unpaid_invoice(booking)
        if not invoice:
            raise ValueError("All payments for this booking have already been completed.")

        payment_amount = self._get_payment_amount(booking)
        if GroupInvoiceService.available_balance < payment_amount:
            raise ValueError(
                "Insufficient balance. "
                f"Available: {GroupInvoiceService.available_balance}, "
                f"required: {payment_amount}."
            )

        with transaction.atomic():
            GroupInvoiceService.available_balance -= payment_amount
            invoice.payment_status = PaymentStatus.PAID
            invoice.save(update_fields=["payment_status"])

        return PayNowResponse.from_model(invoice).to_dict()
