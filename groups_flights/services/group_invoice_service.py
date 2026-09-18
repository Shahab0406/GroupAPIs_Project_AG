from groups_flights.models import GroupFlightsInvoice
from groups_flights.response.invoice import GroupInvoiceDetailResponse


class GroupInvoiceService:
    def get_all_data_from_group_invoice(self, pk: int) -> dict | None:
        invoice = (
            GroupFlightsInvoice.objects.select_related("booking_details__group")
            .filter(pk=pk)
            .first()
        )

        if not invoice:
            return None

        return GroupInvoiceDetailResponse.from_model(invoice).to_dict()
