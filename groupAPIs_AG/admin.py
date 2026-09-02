from django.contrib import admin
from django import forms
from groupAPIs_AG.models import SegmentResearch, Segments

# Register Segments model
admin.site.register(Segments)

class SegmentResearchAdminForm(forms.ModelForm):

    class Meta:
        model = SegmentResearch
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_bound and self.data:
            data = self.data.copy()
            flight_number = data.get("flight_number")

            if flight_number:
                # Get the first record matching the flight_number
                segment = Segments.objects.filter(flight_number=flight_number).first()

                if segment:
                    if not data.get("arrival_datetime_0") and segment.arrival_datetime:
                        data["arrival_datetime_0"] = segment.arrival_datetime.strftime("%Y-%m-%d")

                    if not data.get("arrival_datetime_1") and segment.arrival_datetime:
                        data["arrival_datetime_1"] = segment.arrival_datetime.strftime("%H:%M:%S")

                    if not data.get("departure_datetime_0") and segment.departure_datetime:
                        data["departure_datetime_0"] = segment.departure_datetime.strftime("%Y-%m-%d")

                    if not data.get("departure_datetime_1") and segment.departure_datetime:
                        data["departure_datetime_1"] = segment.departure_datetime.strftime("%H:%M:%S")

                    if not data.get("origin"):
                        data["origin"] = segment.origin

                    if not data.get("destination"):
                        data["destination"] = segment.destination

                    if not data.get("operating_airline"):
                        data["operating_airline"] = segment.operating_airline

                    if not data.get("marketing_airline"):
                        data["marketing_airline"] = segment.marketing_airline

                    self.data = data


@admin.register(SegmentResearch)
class SegmentsResearchAdmin(admin.ModelAdmin):
    form = SegmentResearchAdminForm

    list_display = (
        "flight_number",
        "arrival_datetime",
        "departure_datetime",
        "origin",
        "destination",
        "operating_airline",
        "marketing_airline",
    )
    search_fields = ("flight_number",)

    class Media:
        js = ("management/JS/autofill_flight.js",)