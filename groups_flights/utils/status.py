from django.db import models


class BookingStatus(models.TextChoices):
    ON_HOLD = "on_hold", "On Hold"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"

class InvoiceStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    POSTED = "posted", "Posted"
    FAILED = "failed", "Failed"

class PaymentStatus(models.TextChoices):
    empty = "---", "---" 
    TOKEN_PAYMENT = "token payment", "Token Payment"
    FULL_PAYMENT = "full payment", "Full Payment"