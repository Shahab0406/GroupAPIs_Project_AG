from django.db import models


class BookingStatus(models.TextChoices):
    ON_HOLD = "on_hold", "On Hold"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
