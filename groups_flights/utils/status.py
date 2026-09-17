from django.db import models


class BookingStatus(models.TextChoices):
    ON_HOLD = "ON_HOLD", "ON_HOLD"
    CONFIRMED = "CONFIRMED", "CONFIRMED"
    CANCELLED = "CANCELLED", "CANCELLED"

class InvoiceStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    POSTED = "posted", "Posted"
    FAILED = "failed", "Failed"

class PaymentStatus(models.TextChoices):
    UNPAID = "unpaid", "Unpaid"
    PAID = "paid", "Paid"