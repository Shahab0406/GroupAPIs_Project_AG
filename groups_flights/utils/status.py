from django.db import models


class BookingStatus(models.TextChoices):
    ON_HOLD = "on_hold", "On Hold"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"

class InvoiceStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"

class PaymentStatus(models.TextChoices):
    empty = "---", "---" 
    TOKEN_PAYMENT = "token", "Token Payment"
    FULL_PAYMENT = "full", "Full Payment"