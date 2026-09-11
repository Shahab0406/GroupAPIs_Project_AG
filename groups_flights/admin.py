from django.contrib import admin 
from django import forms

from .models import Flight, Group, GroupBookingDetail, Segment

class FlightAdminForm(forms.ModelForm):

    class Meta:
        model = Flight
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_bound and self.data:
            # Create a mutable copy of form data
            prefix = self.prefix + "-" if self.prefix else ""
            flight_key = f"{prefix}flight_number"
            flight_number = self.data.get(flight_key)

            if flight_number:
                segment = Segment.objects.filter(
                    flight_number=flight_number
                ).first()

                if segment:
                    data = self.data.copy()

                    # Map SplitDateTimeWidget fields (_0 = Date, _1 = Time)
                    if (
                        not data.get(f"{prefix}departure_datetime_0")
                        and segment.departure_datetime
                    ):
                        data[f"{prefix}departure_datetime_0"] = (
                            segment.departure_datetime.strftime("%Y-%m-%d")
                        )

                    if (
                        not data.get(f"{prefix}departure_datetime_1")
                        and segment.departure_datetime
                    ):
                        data[f"{prefix}departure_datetime_1"] = (
                            segment.departure_datetime.strftime("%H:%M:%S")
                        )

                    if (
                        not data.get(f"{prefix}arrival_datetime_0")
                        and segment.arrival_datetime
                    ):
                        data[f"{prefix}arrival_datetime_0"] = (
                            segment.arrival_datetime.strftime("%Y-%m-%d")
                        )

                    if (
                        not data.get(f"{prefix}arrival_datetime_1")
                        and segment.arrival_datetime
                    ):
                        data[f"{prefix}arrival_datetime_1"] = (
                            segment.arrival_datetime.strftime("%H:%M:%S")
                        )

                    # Map Segment 'origin' -> Flight 'sector_from'
                    if not data.get(f"{prefix}origin") and hasattr(
                        segment, "origin"
                    ):
                        data[f"{prefix}origin"] = segment.origin

                    # Map Segment 'destination' -> Flight 'sector_to'
                    if not data.get(f"{prefix}destination") and hasattr(
                        segment, "destination"
                    ):
                        data[f"{prefix}destination"] = segment.destination

                    self.data = data

# ==========================================================================================================

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
    )

    class Media:
        js = ("admin/js/autofill_flight.js",)


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

    class Media:
        js = ("admin/js/autofill_flight.js",)

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
        "is_published",
    )
    list_filter = ("is_active", "is_published")
    search_fields = ("group_name", "pnr")
    inlines = [FlightInline]




@admin.register(GroupBookingDetail)
class GroupBookingDetailAdmin(admin.ModelAdmin):
    list_display = (
        "group",
        "flight",
        "status",
        "adult_seats_requested",
        "child_seats_requested",
        "total_amount",
        "token_payment_deadline",
        "full_payment_deadline",
    )
    list_filter = ("status",)
    search_fields = ("group__group_name", "group__pnr")


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


# ========================================================================================================

