import re

from django.contrib import admin, messages
from django import forms
from django.forms.widgets import Media

from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Airline, Flight, GroupFlightsInvoice, Segment, BookingStatus

from .models import Flight, Group, GroupBookingDetail, Segment

class FlightAdminForm(forms.ModelForm):

    class Meta:
        model = Flight
        fields = "__all__"
        widgets = {
            "departure_datetime": AdminSplitDateTime(),
            "arrival_datetime": AdminSplitDateTime(),
        }

    class Media:
        js = ("admin/js/autofill_flight.js",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mark non-segment fields as optional during initialization
        for field in ("baggage_allowance", "group"):
            if field in self.fields:
                self.fields[field].required = False

        # Backend fallback autofill on POST submission
        if self.is_bound and self.data:
            prefix = f"{self.prefix}-" if self.prefix else ""
            raw_flight_number = self.data.get(f"{prefix}flight_number")

            if raw_flight_number:
                # Clean input (e.g., "zh 306" -> "ZH306")
                clean_str = re.sub(
                    r"[^A-Z0-9]", "", str(raw_flight_number).upper()
                )

                # Format to example ("ZH-306") and extract code "ZH"
                match = re.match(r"^([A-Z]+)(\d+)$", clean_str)
                if match:
                    carrier_code, number = match.groups()
                    formatted_flight_number = f"{carrier_code}-{number}"
                else:
                    carrier_code = "".join(filter(str.isalpha, clean_str))
                    formatted_flight_number = clean_str

                data = self.data.copy()

                # 1. Primary: Lookup Segment using formatted flight number ("ZH-306")
                segment = Segment.objects.filter(
                    flight_number__iexact=formatted_flight_number
                ).first()

                if segment:
                    if not data.get(f"{prefix}airline") and getattr(
                        segment, "airline_id", None
                    ):
                        data[f"{prefix}airline"] = segment.airline_id

                    if not data.get(f"{prefix}origin"):
                        data[f"{prefix}origin"] = segment.origin

                    if not data.get(f"{prefix}destination"):
                        data[f"{prefix}destination"] = segment.destination

                    if segment.departure_datetime:
                        data.setdefault(
                            f"{prefix}departure_datetime_1",
                            segment.departure_datetime.strftime("%H:%M:%S"),
                        )

                    if segment.arrival_datetime:
                        data.setdefault(
                            f"{prefix}arrival_datetime_1",
                            segment.arrival_datetime.strftime("%H:%M:%S"),
                        )
                else:
                    # 2. Fallback: Auto-fill Airline using prefix "ZH" directly from Airline table
                    if carrier_code and not data.get(f"{prefix}airline"):
                        airline = Airline.objects.filter(
                            code__iexact=carrier_code
                        ).first()
                        if airline:
                            data[f"{prefix}airline"] = airline.id

                self.data = data
#=================================================================================================================================================================

def get_permission_media(media, request):
    """Helper function to inject JavaScript only for superusers who are staff."""
    user = getattr(request, "user", None)
    if (
        user
        and user.is_authenticated
        and user.is_superuser
        and user.is_staff
    ):
        return media + Media(js=["admin/js/autofill_flight.js"])
    return media


class FlightInline(admin.TabularInline):
    model = Flight
    form = FlightAdminForm
    extra = 1
    fields = (
        "flight_number",
        "departure_datetime",
        "origin",
        "arrival_datetime",
        "destination",
        "travel_class",
        "baggage_allowance",
        "meal_available",
        "airline",
    )

    # readonly_fields = ("airline")

    def get_media(self, request):
        media = super().get_media(request)
        return get_permission_media(media, request)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    form = FlightAdminForm
    list_display = (
        "flight_number",
        "group",
        "origin",
        "destination",
        "departure_datetime",
        "travel_class",
    )
    list_filter = ("travel_class", "meal_available")
    search_fields = ("flight_number", "origin", "destination")

    def get_media(self, request):
        media = super().get_media(request)
        return get_permission_media(media, request)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [FlightInline]
    list_display = (
        "group_name",
        "pnr",
        "adult_seats",
        "available_adult_seats",
        "child_seats",
        "available_child_seats",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("group_name", "pnr")

    def get_media(self, request):
        media = super().get_media(request)
        return get_permission_media(media, request)


@admin.register(GroupBookingDetail)
class GroupBookingDetailAdmin(admin.ModelAdmin):
    list_display = (
        "group",
        "status",
        "adult_seats_requested",
        "child_seats_requested",
        "total_amount",
        "token_payment_deadline",
        "full_payment_deadline",
    )
    list_filter = ("status",)
    search_fields = ("group__group_name", "group__pnr")

    def save_model(self, request, obj, form, change):
        previous_status = None
        if change and obj.pk:
            previous_status = (
                GroupBookingDetail.objects.filter(pk=obj.pk)
                .values_list("status", flat=True)
                .first()
            )

        super().save_model(request, obj, form, change)

        if (
            previous_status
            and previous_status != BookingStatus.CANCELLED
            and obj.status == BookingStatus.CANCELLED
        ):
            self.message_user(
                request,
                (
                    f"Released {obj.adult_seats_requested} adult and "
                    f"{obj.child_seats_requested} child seat(s) back to "
                    f"{obj.group.group_name}."
                ),
                messages.SUCCESS,
            )

@admin.register(GroupFlightsInvoice)
class GroupFlightsInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "booking_details",
        "invoice_status",
        "payment_status",
        "financial_profile",
        "payment_deadline",
    )
    list_filter = ("invoice_status", "payment_status")
    search_fields = ("invoice_number","booking_details__group__group_name")

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = (
        "flight_number",
        "origin",
        "destination",
        "departure_datetime",
        "arrival_datetime",
    )
    search_fields = ("flight_number",)

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'alias',
        'slug',
        'airline_numeric_code',
        'code',
        'color',
        'has_custom_pricing',
        'logo',
        'is_enabled',
    )
    search_fields = ("name", 'airline_numeric_code')
#=================================================================================================================================================================