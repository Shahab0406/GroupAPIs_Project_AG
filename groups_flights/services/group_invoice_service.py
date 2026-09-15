from groups_flights.models import GroupFlightsInvoice, Group
from groups_flights.response import GroupResponse
from groups_flights.response.group import GroupInvoiceResponse

class GroupInvoiceService:

    def get_all_data_from_group_invoice(self, pk: int) -> dict | None:
        invoice = (
            GroupFlightsInvoice.objects.select_related(
                "group", "booking_details"
            ).filter(pk=pk).first()
        )
        if not invoice:
            return None

        print (GroupInvoiceResponse(invoice).to_dict())

        return (
            GroupInvoiceResponse(invoice).to_dict()
        )
    
invoice_test = GroupInvoiceService()
invoice_test.get_all_data_from_group_invoice(123459)

# "booking_details": {
            #     "id": invoice.booking_details.id,
            #     "flight_number": invoice.booking_details.flight_number,
            #     "passenger_name": invoice.booking_details.passenger_name,
            #     "departure_date": invoice.booking_details.departure_date,
            #     "arrival_date": invoice.booking_details.arrival_date,
            # },

# def get_all_data_from_group_invoice(self, pk: int) -> dict | None:
    #     invoice = GroupFlightsInvoice.objects.select_related("group", "booking_details").filter(pk=pk).first()
    #     if not invoice:
    #         return None
    #     else :
    #         print (invoice.group)
    #         print (invoice.financial_profile)
    #         print (invoice.invoice_number)
    #         print (invoice.booking_details)
    #         print (invoice.status)

    #     return {
    #         "group_invoice": self.map_group_invoice_response(invoice),
    #         "group": GroupInvoiceResponse(invoice).to_dict(),
    #     }

 # def map_group_invoice_response(self, group_invoice) -> dict:
    #     return {
    #         "id": group_invoice.id,
    #         "group_id": group_invoice.group.id,
    #         "invoice_number": group_invoice.invoice_number,
    #         "booking_details_id": group_invoice.booking_details.id,
    #         "status": group_invoice.status,
    #         "financial_profile": group_invoice.financial_profile,
    #     }