from django.contrib import admin

from .models import Flight, Group


class FlightInline(admin.TabularInline):
    model = Flight
    extra = 1


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "group_name",
        "pnr",
        "seats",
        "child_seats",
        "is_active",
        "is_published",
    )
    list_filter = ("is_active", "is_published")
    search_fields = ("group_name", "pnr")
    inlines = [FlightInline]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "flight_number",
        "group",
        "sector_from",
        "sector_to",
        "departure_datetime",
        "travel_class",
    )
    list_filter = ("travel_class", "meal_available")
    search_fields = ("flight_number", "sector_from", "sector_to")
