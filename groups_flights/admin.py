from django.contrib import admin 
from django import forms
from django.forms.widgets import Media

from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.admin.widgets import AdminSplitDateTime
from .models import Flight, Segment

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
            flight_number = self.data.get(f"{prefix}flight_number")

            if flight_number:
                segment = Segment.objects.filter(
                    flight_number=flight_number
                ).first()

                if segment:
                    data = self.data.copy()

                    # Set standard flight segment fields if empty
                    if not data.get(f"{prefix}origin"):
                        data[f"{prefix}origin"] = segment.origin

                    if not data.get(f"{prefix}destination"):
                        data[f"{prefix}destination"] = segment.destination

                    # Split datetime handling (_0 = Date, _1 = Time)
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
    )

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
        "is_published",
    )
    list_filter = ("is_active", "is_published")
    search_fields = ("group_name", "pnr")

    def get_media(self, request):
        media = super().get_media(request)
        return get_permission_media(media, request)


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
#=================================================================================================================================================================