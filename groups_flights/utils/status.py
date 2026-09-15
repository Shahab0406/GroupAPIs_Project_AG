from django.db import models


class BookingStatus(models.TextChoices):
    ON_HOLD = "ON_HOLD", "ON_HOLD"
    CONFIRMED = "CONFIRMED", "CONFIRMED"
    CANCELLED = "CANCELLED", "CANCELLED"
