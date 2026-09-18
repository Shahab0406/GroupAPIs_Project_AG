from django.db import models


class BookingStatus(models.TextChoices):
    ON_HOLD = "ON_HOLD", "ON_HOLD"
    CONFIRMED = "CONFIRMED", "CONFIRMED"
    CANCELLED = "CANCELLED", "CANCELLED"

class InvoiceStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    POSTED = "POSTED", "POSTED"
    FAILED = "FAILED", "FAILED"


class PaymentStatus(models.TextChoices):
    UNPAID = "UNPAID", "UNPAID"
    PAID = "PAID", "PAID"