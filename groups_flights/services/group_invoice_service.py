from groups_flights.models import GroupFlightsInvoice, Group
from groups_flights.response import GroupResponse

class GroupInvoiceService:

    def _serialize_invoice(self, invoice: GroupFlightsInvoice) -> dict:
        group_obj = getattr(invoice.booking_details, "group", None)

        return {
            "group_invoice": {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "invoice_status": invoice.invoice_status,
                "payment_status": invoice.payment_status,
                "financial_profile": invoice.financial_profile,
            },
            "group": (
                {
                    "id": group_obj.id,
                    "invoice_number": invoice.invoice_number,
                    "group_name": getattr(group_obj, "group_name", None),
                }
                if group_obj
                else None
            ),
            "booking_details": (
                {
                    "id": invoice.booking_details.id,
                    "group_name": getattr(group_obj, "group_name", None),
                    "status": getattr(invoice.booking_details, "status", None),
                }
                if invoice.booking_details
                else None
            ),
        }

    def get_all_data_from_group_invoice(self, pk: int) -> dict | None:
        invoice = (
            GroupFlightsInvoice.objects.select_related("booking_details__group")
            .filter(pk=pk)
            .first()
        )

        if not invoice:
            return None

        return self._serialize_invoice(invoice)